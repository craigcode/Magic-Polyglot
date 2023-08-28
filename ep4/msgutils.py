import os
import typer
from dotenv import load_dotenv
from send_sms import send_sms
from send_email_sg import send_email_sg
from send_email_ses import send_email_ses


app = typer.Typer(add_completion=False)


@app.command("sms")
def sms(recipient_number:str,text_message:str):
    '''Send sms via Twilio'''

    send_sms(recipient_number,text_message)


@app.command("sendgrid")
def sendgrid(recipient:str):
    '''Send email via SendGrid'''

    from_email='craig@craigmartin.com'
    to_emails=recipient
    subject='Sending Email with Twilio SendGrid is Fun'
    html_content='<strong>and easy to do anywhere, even with Python</strong>'

    send_email_sg(from_email,to_emails,subject,html_content)


@app.command("ses")
def ses():
    '''Send email via AWS SES'''

    sender=os.environ.get('AWS_SES_SENDER_EMAIL')
    recipient='craig@craigmartin.com'
    subject='Sending Email with Twilio SendGrid is Fun'
    html_content='<h1>Hello World!!</h1><p>This is a pretty mail with HTML formatting</p>'
    plain_text='This is for those who cannot read HTML.'

    send_email_ses(sender,recipient,subject,html_content,plain_text)


@app.command("version")
def version():
    '''Version information'''
    
    version_string = 'v1.00 (08/27/2023)'

    print(f'Magic-Polyglot MsgUtils {version_string}')


if __name__ == "__main__":
    
    load_dotenv()
    app()