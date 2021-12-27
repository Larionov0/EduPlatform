from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', primary_key=True)

    @classmethod
    def create_from_user(cls, user):
        return cls.objects.create(user=user)

    def __str__(self):
        return f"Profile {self.user}"
