from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from apps.auth_module import models as accounts_models
import random
import threading


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def get_or_create_otp(user):
        otp, _ = accounts_models.Otp.objects.get_or_create(
            user=user, defaults={"code": random.randint(100000, 999999)}
        )
        return otp

    @staticmethod
    def send_activation_otp(user):
        otp = Util.get_or_create_otp(user)

        subject = "Verify your email"
        message = render_to_string(
            "email-activation.html",
            {
                "name": user.full_name,
                "otp": otp.code,
            },
        )

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    @staticmethod
    def send_password_change_otp(user):
        otp = Util.get_or_create_otp(user)

        subject = "Your account password reset email"
        message = render_to_string(
            "password-reset.html",
            {
                "name": user.full_name,
                "otp": otp.code,
            },
        )

        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    @staticmethod
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

    @staticmethod
    def match_created(user):
        subject = "Match Created!"
        message = render_to_string(
            "match_created.html",
            {
                "name": user.full_name,
            },
        )
        email_message = EmailMessage(subject=subject, body=message, to=[user.email])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()
