from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IDENTITY_CHOICES = (('S', 'Student'),('T', 'Private Tutor'),('C', 'Contracted Tutor'))
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default='S')
    school = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    courses = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    wallet = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    subjects = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Reset_token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=30, blank=True)
    def __str__(self):
        return self.user.username