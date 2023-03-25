import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from key import news_api_key, gmail_address, gmail_password
import requests
import json


def __gather_articles(country):
    url = ('https://newsapi.org/v2/top-headlines?'
           f'country={country}&'
           f'apiKey={news_api_key}')
    response = requests.get(url)
    return response.json()


def __format_articles_html(news_dict, language):

    head = f"""
            <html>
                <head>
                    <style>
                    .title {{
                        font-weight: bold;
                    }}
                    .articleDiv {{
                        border: 1px outset black;
                    }}
                    .thumbnail {{
                        direction: {'rtl' if language=='ar' else 'ltr'}
                    }}
                    .thumbnail img {{
                        height: 150px;
                        padding: 10px;
                    }}
                    .detail {{
                        direction: {'rtl' if language=='ar' else 'ltr'};
                        padding-left: 10px;
                        padding-right: 10px;
                        padding-bottom: 10px;
                    }}
                    </style>
                </head>
                <body>"""

    body = ""
    for article in news_dict['articles']:

        website = article['url']
        image = article['urlToImage']
        title = article['title']
        description = article['description']
        author = article['author']
        pub_time = article['publishedAt']

        body += """<div class="articleDiv">"""

        if image:
            body += f"""<div class="thumbnail"> <img src="{image}"/> </div>"""

        body += """<div class="detail">"""
        body += f"""<p class="title">{title}</p>"""
        if description:
            body += f"""<p class="description">{description}</p>"""
        if author:
            body += f"""<p class="author">{'بقلم' if language=='ar' else 'Written by'}: {author}</p>"""
        if pub_time:
            body += f"""<p class="publish_date">{'نشر بتاريخ' if language=='ar' else 'Published'}: { pub_time.split('T')[0]}</p>"""
        body += f"""<a href="{website}">{'المزيد...' if language=='ar' else 'More...'}</a> </div> </div>"""

    tail = "</body></html>"

    return head + body + tail


def __connect_to_server(sender, password):
    print("Connecting to server...")
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # server and port
    smtp_server.login(sender, password)
    print("Succesfully connected to server\n")
    return smtp_server


def send_email(sender, password, reciever_list, subject, content):
    # Connect to SMTP server
    smtp_server = __connect_to_server(sender, password)

    msg = MIMEText(content)
    msg['subject'] = subject
    msg['from'] = "Daily Newsletter"

    for reciever in reciever_list:

        del msg['To']
        msg['to'] = reciever

        print(f"Sending email to : {reciever}...")
        smtp_server.sendmail(sender, reciever, msg.as_string())
        print(f"Email sent to: {reciever}.\n")

    smtp_server.quit()


def __send_newsletter(smtp_server, sender, reciever_list, country, language):

    # Gather and format articles
    news = __gather_articles(country)
    formatted_news = __format_articles_html(news, language)

    # Create MIME object to define different parts of our email
    msg = MIMEMultipart()
    msg['From'] = "Daily Newsletter"
    msg['Subject'] = '📰 Your daily newsletter from Youssef Kadry'

    # Attach body to mesage
    msg.attach(
        MIMEText("Here is your daily drop of fresh news!\n\n", 'plain'))
    msg.attach(MIMEText(formatted_news, 'html'))
    msg.attach(
        MIMEText(f"\n\nTo unsubscribe send an email with the subject 'unsubscribe' to {sender}", 'plain'))

    # Send email to all recipients
    for reciever in reciever_list:

        del msg['To']
        msg['To'] = reciever

        print(f"Sending newsletter to : {reciever}...")
        smtp_server.sendmail(sender, reciever, msg.as_string())
        print(f"Newsletter sent to: {reciever}.\n")


def send_newsletter_all_channels(sender, password):

    subs = json.load(open("subscribers.json", "r"))

    # Connect to SMTP server
    smtp_server = __connect_to_server(sender, password)

    for channel in subs:
        country, language = channel.split(',')
        __send_newsletter(smtp_server, sender,
                          subs[channel], country, language)

    smtp_server.quit()


def send_newsletter_channels(sender, password, channel_list):

    subs = json.load(open("subscribers.json", "r"))

    # Connect to SMTP server
    smtp_server = __connect_to_server(sender, password)

    for channel in channel_list:
        if channel in subs:
            country, language = channel.split(',')
            __send_newsletter(smtp_server, sender,
                              subs[channel], country, language)

    smtp_server.quit()


if __name__ == "__main__":
    # send_newsletter_all_channels(
    #     gmail_address, gmail_password)
    send_email(gmail_address, gmail_password,
               ['youssefamr2008@gmail.com'], "Unsubscription", "It appears you unsubscribed from the newsletter")
