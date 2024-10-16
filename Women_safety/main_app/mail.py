import smtplib
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




# Before using your email,  please ensure that you have set you gmail account to enable "less secure apps"
# Recheck this step that you have enabled the less secure app

def send_email(name, dest, link,data):
    try:
        with open("main_app/templates/main_app/email.html", "r") as email_html:
            email_body = email_html.read().format(name=name, link=link , data=data)

        server = smtplib.SMTP("smtp.gmail.com", 587)  # Gmail SMTP port (TLS)
        server.ehlo()
        server.starttls()
        server.login('abhysihdes001@gmail.com','eqbffupvvvmuncls')


        # # Use an App Password instead of your main account password
        # server.login("abhysihdes001@gmail.com", "eqbffupvvvmuncls")

        msg = MIMEMultipart()
        msg["Subject"] = "EMERGENCY"
        msg.attach(MIMEText(email_body, "html"))

        
        
        # Set the sender email
        msg["From"] = formataddr(("TEAM WOMEN SAFETY", "abhysihdes001@gmail.com"))

        # Send the email
        server.sendmail("abhysihdes001@gmail.com", dest, msg.as_string())
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error sending email: {e}")
