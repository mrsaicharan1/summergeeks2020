import os
from config import SENDGRID_API_KEY, address
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(to_email, subject, html_content):
    """ 
    Sendgrid API module
    """
    message = Mail(
    from_email='saicharan.reddy1@gmail.com',
    to_emails=to_email,
    subject=subject,
    html_content=html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)
   
