import os
import datetime

#os.system("python manage.py runserver &")

while(1):
    currentTime = datetime.datetime.now()
    if (currentTime.minute == 30 or currentTime.minute == 0) and (currentTime.second == 0 and currentTime.microsecond == 0):
        os.system("python manage.py all_sessions")