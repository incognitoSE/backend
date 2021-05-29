from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta
from django.conf import settings
import jdatetime


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("User should have an email address!")

        email = self.normalize_email(email.lower())
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return f"{self.email}"


class UserHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    model = models.CharField(max_length=15)
    data = models.CharField(max_length=150)
    price = models.IntegerField()
    date = models.CharField(max_length=40)


class UserTransactions(models.Model):
    TYPE_CHOICES = (("ch", "افزایش اعتبار"), ("se", "استفاده از سرویس"))
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    service = models.CharField(max_length=150, default="-")
    amount = models.IntegerField()
    date = models.CharField(max_length=40)


class UserWallet(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    trial = models.IntegerField(default=2)


class Notifications(models.Model):
    text = models.TextField()
    date = models.CharField(max_length=50, default=jdatetime.datetime.now().strftime("%d/%m/%Y"))

    def __str__(self):
        return f"{self.date}"