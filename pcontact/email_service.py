from django.core.mail import send_mail,send_mass_mail,mail_admins
from .email_config import EmailConfig

class EmailService:
    def __init__(self):
        pass
    
    @classmethod
    def send_email(cls,sender,receiver_list,data=None):
        """ @sender is the name of person who send email,\n 
            @receiver_list is a l ofist person who will receive message\n
            @data["sender_email"] contain the meail of sender\n
            @data["password"] is the authentification password\n
            @data["subject"] contain the subject of message\n
            @data["msg"] contain the message of the mail """
        #print("Nous sommes dans les emails")
        try:
            password=EmailConfig.emails[data["sender_email"]]
            #print(password)
            send_mail(
                  subject=data["subject"],
                  message=data["msg"],
                  from_email=data["sender_email"],
                  recipient_list=receiver_list,
                  auth_user=data["sender_email"],
                  auth_password=password,
                  html_message=data["msg"])
            #print("mail sendeed")
            return True
        except Exception as e:
            #print("bonjour la famille")
            #print(e)
            return False