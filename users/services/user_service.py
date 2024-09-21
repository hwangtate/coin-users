from users.models import User


class UserService:

    @staticmethod
    def user_email_confirmed(user: User) -> None:
        user.is_active = True
        user.email_confirmed = True
        user.save()
