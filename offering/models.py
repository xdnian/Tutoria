from django.db import models
from django.contrib.auth.models import User
import pytz

TIMEZONELOCAL = pytz.timezone('Asia/Hong_Kong')

# Create your models here.
class Timeslot(models.Model):
    # Possible status:
    # Available, Booked, Unavailable, Blocked
    global TIMEZONELOCAL
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20, default='Available')

    def __str__(self):
        startlocal = self.start.astimezone(TIMEZONELOCAL)
        endlocal = self.end.astimezone(TIMEZONELOCAL)
        date = startlocal.strftime('%Y-%m-%d')
        time = startlocal.strftime('%H:%M')  + ' ~ ' + endlocal.strftime('%H:%M')
        return self.tutor.username + ' ' + date + ' ' + time + ' price: $' + str(self.tutor.tutorprofile.price)
