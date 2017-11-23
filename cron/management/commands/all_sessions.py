from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from booking.models import Session
from offering.models import Timeslot
from home.models import Notification
from transaction.models import Transaction
import datetime, decimal
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

        allBookedSessions = Session.objects.filter( Q(timeslot__start__lte=tomorrowTime, status = 'Booked')).order_by('start')
        for session in allBookedSessions:
            session.status = 'Committed'
            session.save()

        allStartedSessions = Session.objects.filter( Q(timeslot__start__lte=currentTime, status = 'Committed')).order_by('start')
        for session in allBookedSessions:
            session.status = 'Started'
            session.save()

        # End all sessions
        allFinishedSessions = Session.objects.filter (Q(timeslot__end__lte=currentTime, status = 'Started')).order_by('end')
        for session in allFinishedSessions:
            session.status = 'Ended'
            price = session.transaction0.amount
            commission = session.commission
            session.timeslot.tutor.profile.wallet.addBalance(price-commission)
            utcCurrentTime = timezone.now()
            timezonelocal = pytz.timezone('Asia/Hong_Kong')
            currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
            new_transaction = Transaction(from_wallet = medium.profile.wallet, to_wallet = session.timeslot.tutor.profile.wallet, 
                time = currentTime, amount = price-commission, description = 'Tutorial payment')
            new_transaction.save()
            session.transaction1 = new_transaction
            
            MyTutors = User.objects.get(username='MyTutors')
            MyTutors.profile.wallet.addBalance(commission)
            new_transaction = Transaction(from_wallet = medium.profile.wallet, to_wallet = MyTutors.profile.wallet, 
                time = currentTime, amount = commission, description = 'Commission fee')
            new_transaction.save()
            medium = User.objects.get(username='admin')
            medium.profile.wallet.withdraw(price)
            Notification(session.timeslot.tutor, 'A tutorial session fee of HK$' + str(price) + ' had been added to your wallet.')
            Notification(session.student, 'You are invited to write a review for this tutorial session.')
            session.save()
