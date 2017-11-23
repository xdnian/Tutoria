from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from', null=True)
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to', null=True)
    message = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
