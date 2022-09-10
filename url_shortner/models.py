import datetime

from django.db import models
from django.contrib.auth.models import User
from random import choices
from string import ascii_letters
from django.conf import settings
from rest_framework.permissions import AllowAny


# Create your models here.

class Link(models.Model):
    original_link = models.URLField()
    shortened_link = models.URLField(blank=True, null=True)
    creation_date = models.DateField(auto_now=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    private = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, unique=False)

    def __str__(self):
        return self.original_link

    def shortener(self):

        while True:
            random_string = ''.join(choices(ascii_letters, k=6))
            new_link = settings.HOST_URL + '/' + random_string

            if not Link.objects.filter(shortened_link=new_link).exists():
                break

        return new_link

    def save(self, *args, **kwargs):
        if not self.shortened_link:
            new_link = self.shortener()
            self.shortened_link = new_link
        if not self.expiration_date:
            self.expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)

        return super().save(*args, **kwargs)
