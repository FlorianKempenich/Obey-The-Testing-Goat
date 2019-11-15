from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token

# # Ensures we correctly registered our model with the
# # 'authentication' app
User = get_user_model()


class UserModelTest(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()  # Should not raise

    def test_email_is_primary_key(self):
        user = User(email='a@b.com')
        user.save()

        self.assertEqual(
            User.objects.get(pk='a@b.com'),
            user
        )


class TokenModelTest(TestCase):
    def test_links_user_with_auto_generated_uid(self):
        token1 = Token.objects.create(email='a@b.com')
        token2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(token1.uid, token2.uid)