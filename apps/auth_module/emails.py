from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from . import models as accounts_models
import random, threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    def send_activation_otp(user):
        subject = "Verify your email"
        code = random.randint(100000, 999999)
        message = render_to_string(
            "email-activation.html",
            {
                "name": user.full_name,
                "otp": code,
            },
        )
        otp = accounts_models.Otp.objects.get_or_none(user=user)
        if not otp:
            accounts_models.Otp.objects.create(user=user, code=code)
        else:
            otp.code = code
            otp.save()

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    def send_password_change_otp(user):
        subject = "Your account password reset email"
        code = random.randint(100000, 999999)
        message = render_to_string(
            "password-reset.html",
            {
                "name": user.full_name,
                "otp": code,
            },
        )
        otp = accounts_models.Otp.objects.get_or_none(user=user)
        if not otp:
            accounts_models.Otp.objects.create(user=user, code=code)
        else:
            otp.code = code
            otp.save()

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"

        EmailThread(email_message).start()

    def password_reset_confirmation(user):
        subject = "Password Reset Successful!"
        message = render_to_string(
            "password-reset-success.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    @staticmethod
    def welcome_email(user):
        subject = "Account verified!"
        message = render_to_string(
            "welcome.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()