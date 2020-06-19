import binascii
import os
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from .validators import over_18


class Post(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Post: {self.author} / {self.created}'

    def save(self, *args, **kwargs):
        if self.id:
            PostEditHistory.objects.create(post=self, author=self.author, text=self.text,
                                           timestamp=datetime.timestamp(self.updated))
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-updated', )


class PostEditHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.PositiveIntegerField()

    def __str__(self):
        return f'Post History: {self.author} / {datetime.fromtimestamp(self.timestamp)}'

    class Meta:
        ordering = ('timestamp',)


class CustomUser(User):
    bio = models.TextField()
    birth_date = models.DateField(validators=[over_18])
    rating = models.IntegerField(default=0)
    show_in_search_results = models.IntegerField(default=0)

    '''PointField doesnt work on my kubuntu( '''
    lat = models.DecimalField('Latitude', max_digits=10, decimal_places=8)
    lng = models.DecimalField('Longitude', max_digits=11, decimal_places=8)

    '''I think is better use ForeignKey to sex model, not choices'''
    OTHER, MALE, FEMALE = 0, 1, 2
    SEX_CHOICES = [
        (OTHER, 'Other'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    sex = models.SmallIntegerField(choices=SEX_CHOICES)

    class Meta:
        ordering = ('last_name', )


class CustomToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField("Key", max_length=40, primary_key=True)

    user = models.OneToOneField(CustomUser, related_name='custom_auth_token', on_delete=models.CASCADE)
    created = models.DateTimeField("Created", auto_now_add=True)

    def __str__(self):
        return self.key

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(CustomToken, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"


