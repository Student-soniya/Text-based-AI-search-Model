from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_person = models.CharField(max_length=10)
    chat = models.CharField(max_length=1000)
