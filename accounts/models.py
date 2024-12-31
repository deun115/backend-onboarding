from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, nickname, password=None):
        if not nickname:
            raise ValueError('Users Must Have a nickname')

        user = self.model(nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(nickname, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Users(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    password = models.CharField(null=False, max_length=128)
    nickname = models.CharField(null=False, max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "users"
