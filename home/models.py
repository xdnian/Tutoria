from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Wallet

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IDENTITY_CHOICES = (('S', 'Student'),('T', 'Private Tutor'),('C', 'Contracted Tutor'))
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default='S')
    SCHOOL_CHOICES = (('1', 'University of Hong Kong'),('2', 'Hong Kong University of Science and Technology'),
        ('3', 'Chinese University of Hong Kong'), ('4', 'City University of Hong Kong'), 
        ('5', 'The Hong Kong Polytechnic University'), ('6', 'Hong Kong Baptist University'))
    school = models.CharField(max_length=2, choices=SCHOOL_CHOICES, default='1')
    phone = models.CharField(max_length=30)
    courses = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True, related_name='tutor')
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