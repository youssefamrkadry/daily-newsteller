import email
import imaplib
import email_sender
import json
from key import gmail_address, gmail_password


def __retrieve_unseen_email(sender_email, password):

    # connect to the server and go to its inbox
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(sender_email, password)
    mail.select('inbox')

    # search for unseen mails
    _, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0].split()

    # mail_ids is a list of bytes that represents searched mails
    return mail, mail_ids


def __process_mail(sender_from, subject: str, my_email, my_password):

    sender_email = sender_from[sender_from.find(
        "<")+1: sender_from.find(">")]

    if "unsubscribe" in subject.lower():
        print(f"Unsubscribing {sender_email} from newsletter")

        subs = json.load(open("subscribers.json", "r"))
        for channel in subs:
            subs[channel].remove(sender_email)
        with open('subscribers.json', 'w') as f:
            json.dump(subs, f)

        email_sender.send_email(my_email, my_password, [sender_email],
                                "Newsletter Unsubscription",
                                "You have been successfully unsubscribed from the newsletter")

        print(f"Unsubscribed {sender_email} from newsletter")

    elif subject.lower() == "subscribe":
        print(f"Subscribing {sender_email} to newsletter")

        subs = json.load(open("subscribers.json", "r"))
        for channel in subs:
            if not sender_email in subs[channel]:
                subs[channel].append(sender_email)
        with open('subscribers.json', 'w') as f:
            json.dump(subs, f)

        email_sender.send_email(my_email, my_password, [sender_email],
                                "Newsletter Subscription",
                                "You have been successfully subscribed to the newsletter")

        print(f"Subscribed {sender_email} to newsletter")


def process_unseen_emails(my_email, my_password):

    mail, mail_ids = __retrieve_unseen_email(my_email, my_password)

    # For every id we'll fetch the email to extract its content
    for i in mail_ids:

        _, data = mail.fetch(i, '(RFC822)')
        # '(RFC822)' format comes on list which includes a tuple with header, content, and the closing byte b')'
        for response_part in data:
            # so if its a tuple...
            if isinstance(response_part, tuple):
                # we go for the content at its second element
                message = email.message_from_bytes(response_part[1])
                __process_mail(
                    message['from'], message['subject'],
                    my_email, my_password)


if __name__ == '__main__':
    process_unseen_emails(gmail_address, gmail_password)
