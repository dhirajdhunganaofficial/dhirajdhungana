import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(name,email,phoneNumber,subject,message):
    # -------- 1. Email Login Details --------
    your_email = "dhirajdhunganaofficial@gmail.com"
    your_app_password = "olhdfdeerxbikfzg"  # NOT your Gmail password!

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
