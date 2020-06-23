from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from .validators import over_18


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.PositiveIntegerField()

    def __str__(self):
        return f'Post History: {self.author} / {datetime.fromtimestamp(self.timestamp)}'

    class Meta:
        ordering = ('timestamp',)


class Profile(models.Model):
    '''For sloving problem with token auth.  (Use: user.profile.bio)'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField()
    birth_date = models.DateField(validators=[over_18])
    rating = models.PositiveIntegerField(default=0)
    show_in_search_results = models.PositiveIntegerField(default=0)

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
        ordering = ('user__last_name', )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
