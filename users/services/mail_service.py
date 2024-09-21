from django.core.mail import send_mail
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from rest_framework import status
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from users.models import User


class EmailService:
    def __init__(self, user: User) -> None:
        self.user = user
        self.email_from = EMAIL_HOST_USER
        self.recipient_list = [user.email]

    def signer(self) -> str:
        signer = TimestampSigner()
        signed_user_email = signer.sign(self.user.email)
        signer_dump = signing.dumps(signed_user_email)
        return signer_dump

    def get_url(self, domain: str, uri: str) -> str:
        back_uri = f"{uri}?code={self.signer()}"
        front_uri = domain
        return f"{front_uri}{back_uri}"

    def send_email(self, subject: str, message: str) -> None:
        send_mail(subject, message, self.email_from, self.recipient_list)

    def send_register_mail(self, activation_url: str) -> None:
        subject = "Confirm your Account"
        message = (
            f"Hi {self.user.nickname},\n\n" f"Please click the link below to confirm your account:\n{activation_url}"
        )

        self.send_email(subject, message)

    @staticmethod
    def decode_signer(code: str) -> str | Response:
        signer = TimestampSigner()

        try:
            decoded_user_email = signing.loads(code)
            email = signer.unsign(decoded_user_email, max_age=60 * 3)
            return email

        except SignatureExpired:
            return Response("expired time...", status=status.HTTP_400_BAD_REQUEST)

    # def send_change_email_mail(self):
    #     uri = "verify"
    #     verification_url = self.get_url(uri)
    #
    #     subject = "Confirm Your Email Change"
    #     message = (
    #         f"Hi {self.user.nickname},\n\n"
    #         f"We received a request to change the email address associated with your account.\n\n"
    #         f"To confirm this change, please click the link below:\n{verification_url}"
    #     )
    #
    #     self.send_email(subject, message)
