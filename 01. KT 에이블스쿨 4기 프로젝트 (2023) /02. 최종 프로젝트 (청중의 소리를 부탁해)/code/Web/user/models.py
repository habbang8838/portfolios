from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, userid):
        return self.get(**{self.model.USERNAME_FIELD: userid})

    def create_user(self, userid, email, name, password=None, **extra_fields):
        """
        Create and save a User with the given userid and password.
        """
        if not userid:
            raise ValueError(_('The User ID must be set'))
        if not email:
            raise ValueError(_('The User Email must be set'))

        email = self.normalize_email(email)
        user = self.model(userid=userid, email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userid, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given userid and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(userid, password, **extra_fields)


class User(AbstractBaseUser):
    userid = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'userid'  # 고식별이 될 필드

    class Meta:
        db_table = "user"

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
