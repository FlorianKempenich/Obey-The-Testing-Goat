from django.db import models
from django.contrib import auth
from uuid import uuid4

auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    @staticmethod
    def exists(email):
        return User.objects.filter(email=email).exists()


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid4, max_length=250)
