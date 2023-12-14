from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, password, **extra_fields):
        if not email:
            raise ValueError('email address must be provided')
        user = self.model(email = self.normalize_email(email), first_name= first_name, last_name=last_name, 
                          username= username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff should be true")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser should be true")
        
        return self.create_user(email, first_name, last_name, username, password, **extra_fields)
    

class MyUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=255, verbose_name="email address")
    first_name = models.CharField(max_length=62)
    last_name = models.CharField(max_length=62)
    username = models.CharField(max_length=255)

    objects= MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.username
    

class Drink(models.Model):
    title = models.CharField(max_length= 255)
    description = models.TextField()
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add= True)
    slug = models.SlugField()

    def __str__(self):
        return self.title