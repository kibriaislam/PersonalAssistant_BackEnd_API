from django.core.mail import EmailMessage



class SendEmail:
    @staticmethod
    def send(data):
        email = EmailMessage( subject= data['email_subject'],body = data['email_body'],to = data['email_to'])
        email.send()