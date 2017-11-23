from django.db import models
from django.contrib.auth.models import User
import pytz
from offering.models import Timeslot
from transaction.models import Transaction

class Session(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='student')
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, null=True, related_name='timeslot')
    status = models.CharField(max_length=10, default='Booked')
    topic = models.CharField(max_length=140, blank=True)
    transaction0 = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, related_name='transaction0')
    transaction1 = models.ForeignKey(Transaction, on_delete=models.CASCADE, null=True, related_name='transaction1')
    commission = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    #review = models.OneToOneField('Review', null = True)
    def __str__(self):
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        startlocal = self.timeslot.start.astimezone(timezonelocal)
        endlocal = self.timeslot.end.astimezone(timezonelocal)
        date = startlocal.strftime('%Y-%m-%d')
        time = startlocal.strftime('%H:%M')  + ' ~ ' + endlocal.strftime('%H:%M')
        return self.status + ' ' + self.timeslot.tutor.username + ' ' + self.student.username  + ' ' + date + ' ' + time + ' price: $' + str(self.timeslot.tutor.tutorprofile.price)
        
class Review(models.Model):
    session = models.OneToOneField(Session, on_delete = models.CASCADE)
    score = models.IntegerField(default = 0)
    comment = models.CharField(max_length = 1000, blank = True)
    isAnonymous = models.BooleanField(default = True)
    # isValid = models.BooleanField(default = False)

    def __str__(self):
        return 'Score: ' + str(self.score) + ' Comment: ' + self.comment + ' isAnonymous: ' + str(self.isAnonymous) # + ' isValid: ' + str(self.isValid)