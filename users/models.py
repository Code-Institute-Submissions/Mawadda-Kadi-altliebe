from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    about_me = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)  # Changed from ForeignKey to CharField
    state = models.CharField(max_length=100, blank=True, null=True)  # New field

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()