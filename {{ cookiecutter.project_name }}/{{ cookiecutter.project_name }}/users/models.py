from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
  first_name = models.CharField(max_length=30, verbose_name='first name')
  last_name = models.CharField(max_length=150, verbose_name='last name')
  email = models.EmailField(unique=True, verbose_name='email address')

  def get_absolute_url(self):
    return reverse("user:detail", kwargs={ "username": self.username })

  def __str__(self):
    return self.username


