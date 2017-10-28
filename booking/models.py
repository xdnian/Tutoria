from django.db import models
from django.contrib.auth.models import User
import pytz

class Session(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='student')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tutor')
    start = models.DateTimeField()
    end = models.DateTimeField()
    def __str__(self):
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        startlocal = self.start.astimezone(timezonelocal)
        endlocal = self.end.astimezone(timezonelocal)
        date = startlocal.strftime('%Y-%m-%d')
        time = startlocal.strftime('%H:%M')  + ' ~ ' + endlocal.strftime('%H:%M')
        return self.tutor.username + ' ' + self.student.username  + ' ' + date + ' ' + time + ' price: $' + str(self.tutor.profile.price)
        