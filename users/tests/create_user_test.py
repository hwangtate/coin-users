from django.test import TestCase

from users.models import User


class CreateUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@test.com", password="qwer1234")

        self.assertEqual(user.email, "test@test.com")  # 아매일 검증
        self.assertNotEqual(user.password, "qwer1234")  # 바말번호 해쉬 검증
        self.assertIsNotNone(user.nickname)  # 유저 난수 이름 생성 검증
        self.assertIsNone(user.social_provider)
        self.assertIsNone(user.ranking)
        self.assertEqual(user.email_confirmed, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="test@test.com", password="qwer1234")

        self.assertEqual(user.email, "test@test.com")  # 아매일 검증
        self.assertNotEqual(user.password, "qwer1234")  # 바말번호 해쉬 검증
        self.assertIsNotNone(user.nickname)  # 유저 난수 이름 생성 검증
        self.assertIsNone(user.social_provider)
        self.assertIsNone(user.ranking)
        self.assertEqual(user.email_confirmed, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_create_social_users(self):
        user = User.objects.create_social_user(email="test@test.com", social_provider="GOOGLE")

        self.assertEqual(user.email, "test@test.com")  # 아매일 검증
        self.assertEqual(user.social_provider, "google")  # choice 검증 (소문자)
        self.assertIsNotNone(user.password)
        self.assertIsNone(user.ranking)
        self.assertEqual(user.email_confirmed, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
