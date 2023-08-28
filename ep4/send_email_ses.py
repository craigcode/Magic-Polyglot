import os
import boto3
from dotenv import load_dotenv


def send_email_ses(sender,recipient,subject,htmltext,plaintext):
    session = boto3.Session(
    aws_access_key_id=os.environ.get('AWS_SES_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SES_SECRET_ACCESS_KEY')
    )
    client = session.client('ses', region_name=os.environ.get('AWS_SES_REGION_NAME'))

    response = client.send_email(
        Destination={
            'ToAddresses': [
                recipient
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': 'UTF-8',
                    'Data': htmltext,
                },
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': plaintext,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=sender,
    )

    print(response)
