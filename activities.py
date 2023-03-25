from temporalio import activity
import email_sender
import email_reciever
from key import gmail_address, gmail_password


@activity.defn
async def send_newsletter():
    email_sender.send_newsletter_all_channels(gmail_address, gmail_password)


@activity.defn
async def check_mail():
    email_reciever.process_unseen_emails(gmail_address, gmail_password)
