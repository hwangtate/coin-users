from typing import Optional, Any

from django.contrib.auth.models import BaseUserManager
from django.db.models import Model

from users.services.nickname_service import TemporaryNickNameService


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> Model:
        email = self.normalize_email(email)

        if "nickname" not in extra_fields:
            tns = TemporaryNickNameService()
            extra_fields["nickname"] = tns.generate_nickname()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> Model:
        extra_fields.setdefault("email_confirmed", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(email, password, **extra_fields)

    def create_social_user(self, email: str, social_provider: Optional[str], **extra_fields: Any) -> Model:
        extra_fields.setdefault("email_confirmed", True)
        extra_fields.setdefault("is_active", True)

        email = self.normalize_email(email)
        social_provider = social_provider.lower()

        if "nickname" not in extra_fields:
            tns = TemporaryNickNameService()
            extra_fields["nickname"] = tns.generate_nickname()

        user = self.model(email=email, social_provider=social_provider, **extra_fields)
        user.set_unusable_password()
        user.save(using=self._db)

        return user
