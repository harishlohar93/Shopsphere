from django.conf import settings
from django.core.mail import send_mail





def send_account_sctivation_email(email_token,email):
    subject = 'Activate your account'
    email_from = settings.EMAIL_HOST_USER
    message = f'Click on the link to verify your email 127.0.0.1:8000/accounts/activate/{email_token}'
    
    # creating route
    send_mail(subject, message, email_from, [email], )
    
    