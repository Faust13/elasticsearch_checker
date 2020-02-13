import smtplib
import config as conf

from jinja2 import Template


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_address = conf.email_from
password = conf.email_passwd
notify_to = conf.email_receivers
alert_subject="test123"
alert_type = "firing"
alert_text = "text"

def read_template(filename):

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    message_template = read_template('alert.j2')

    s = smtplib.SMTP(host='localhost')
    s.starttls()
    
    for email in notify_to:
        msg = MIMEMultipart()

        message = message_template.render(alert_subject=alert_subject, alert_type=alert_type, alert_text=alert_text)

        print(message)

        msg['From']=from_address
        msg['To']=email
        
        
        msg.attach(MIMEText(message, 'html'))
        
        s.send_message(msg)
        del msg
        
    s.quit()