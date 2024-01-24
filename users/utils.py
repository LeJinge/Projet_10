from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user):
    subject = "Vérifiez votre adresse email"
    message = f"Votre code de vérification est {user.email_confirm_token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)
