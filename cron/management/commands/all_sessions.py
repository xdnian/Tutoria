from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone
from booking.models import Session
from offering.models import Timeslot
import datetime
import pytz

class Command(BaseCommand):
    help = 'Begin and end all sessions'

    #def add_arguments(self, parser):
    #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):

        utcCurrentTime = timezone.now()
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
        tomorrowTime = timezone.localtime(utcCurrentTime + datetime.timedelta(hours = 24), timezonelocal)
        
        # Begin all sessioins

        allExpiredTimeslots = Timeslot.objects.filter( Q(start__lte=tomorrowTime, status = 'Available')).order_by('start')
        for timeslot in allExpiredTimeslots:
            timeslot.status = 'Unavailable'
            timeslot.save()

        allBookedTimeslots = Timeslot.objects.filter( Q(start__lte=tomorrowTime, status = 'Booked')).order_by('start')
        for timeslot in allBookedTimeslots:
            timeslot.status = 'Committed'
            timeslot.save()
            #timeslot.delete()
            #timeslot.save()

        allBookedSessions = Session.objects.filter( Q(start__lte=tomorrowTime, status = 'Booked')).order_by('start')
        for session in allBookedSessions:
            session.status = 'Committed'
            session.save()

        allStartedSessions = Session.objects.filter( Q(start__lte=currentTime, status = 'Committed')).order_by('start')
        for session in allBookedSessions:
            session.status = 'Started'
            session.save()

        # End all sessions
        allFinishedSessions = Session.objects.filter (Q(end__lte=currentTime, status = 'Started')).order_by('end')
        for session in allFinishedSessions:
            session.status = 'Ended'
            session.tutor.profile.wallet = session.tutor.profile.wallet + session.tutor.profile.price
            session.tutor.save()
            session.save()
