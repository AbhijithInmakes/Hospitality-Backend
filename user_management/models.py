from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    

class User(AbstractBaseUser):
   
    USER_TYPE_CHOICES = (
        (0, 'User'),
        (1, 'Admin'),
        (2, 'Doctor'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    username = models.CharField(
        max_length=150, 
        unique=False,
        help_text='Required. 150 characters or fewer. Letters, digits, and spaces only.',
        validators=[],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

   
    USERNAME_FIELD = 'email' 
    objects = CustomUserManager()
