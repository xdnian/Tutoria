from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from transaction.models import Wallet
from booking.models import Review
from django.db.models import Count, Avg

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    IDENTITY_CHOICES = (('S', 'Student'),('T', 'Tutor'))
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default='S')
    SCHOOL_CHOICES = (('1', 'University of Hong Kong'),('2', 'Hong Kong University of Science and Technology'),
        ('3', 'Chinese University of Hong Kong'), ('4', 'City University of Hong Kong'), 
        ('5', 'The Hong Kong Polytechnic University'), ('6', 'Hong Kong Baptist University'))
    SCHOOL_CHOICES_DICT = dict((x, y) for x, y in SCHOOL_CHOICES)
    school = models.CharField(max_length=2, choices=SCHOOL_CHOICES, default='1')
    phone = models.CharField(max_length=30)
    picture = models.ImageField(upload_to='static/assets/img/avatar/',
                                default='static/assets/img/avatar/def_avatar.png')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.user.username

    def get_school_name(self):
        return self.SCHOOL_CHOICES_DICT[self.school]

class Tutorprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TUTOR_CHOICES = ('P', 'Private Tutor'),('C', 'Contracted Tutor')
    tutortype = models.CharField(max_length=2, choices=TUTOR_CHOICES, default='P')
    courses = models.TextField(blank=True)
    biography = models.TextField(blank=True) 
    subjects = models.TextField(blank=True)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username

    def get_all_reviews(self):
        return Review.objects.filter(session__timeslot__tutor = self.user)

    def get_review_average(self):
        reviews = self.get_all_reviews()
        # TODO: change to 3
        if len(reviews) < 1:
            return None
        else:
            return reviews.aggregate(Avg('score'))['score__avg']

    def get_formatted_review_average(self):
        avg_score = self.get_review_average()
        if (avg_score is None):
            return 'Insufficient Reviews'
        else:
            avg_score = int(avg_score*2) / 2.0
            return str(avg_score)

    def get_review_average_stars(self):
        avg_score = self.get_review_average()
        if (avg_score is None):
            return []
        else:
            stars = int(avg_score)
            half_stars = int(avg_score*2) % 2
            return [stars*'*', half_stars*'*', (5-stars-half_stars)*'*']


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

class Course_code(models.Model):
    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.code

def Notification(user, message):
    print ('****************************')
    print ("Email to username: " + user.username + " at " + user.email)
    print (message)
    print ('****************************')