import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import boto3
from botocore.exceptions import ClientError
import json

def get_secret():

    secret_name = "email/smtp-credentials"
    region_name = "ap-northeast-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    secret_Dictionary =  json.loads(secret)
    return secret_Dictionary['email'], secret_Dictionary['password']



def sendEmail(botField,name,email,phoneNumber,subject,message):

    if botField and botField.strip():
        return "Email not sent! Bot detected successfully!"

    email, password = get_secret()
    print(email, password)

    # -------- 1. Email Login Details --------
    your_email = email
    your_app_password = password  # NOT your Gmail password!

    # -------- 2. Email Content --------
    contact_name = name
    contact_email = email
    contact_phoneNumber = phoneNumber
    subject = subject + " - Personal Website Alert"

    message = message

    print(message)

    body = f"""
    <html>
    <body>
        <h3>New Message Notification</h3>
        
        <p><strong>Sender Details:</strong></p>
        <ul>
            <li><strong>Name:</strong> {contact_name}</li>
            <li><strong>Phone:</strong> {contact_phoneNumber}</li>
            <li><strong>Email:</strong> {contact_email}</li>
        </ul>
        
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        
        <hr>
        <small>Automated notification - Sent from dhirajdhungana.com</small>
    </body>
    </html>
    """

    # -------- 3. Creating the Email Format --------
    message = MIMEMultipart()
    message["From"] = your_email
    message["To"] = your_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    # -------- 4. Sending the Email --------
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Gmail SMTP server
        server.starttls()  # encrypts the connection
        server.login(your_email, your_app_password)
        server.sendmail(your_email, your_email, message.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Something went wrong:", e)
