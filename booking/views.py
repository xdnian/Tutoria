from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import BookingForm, TutorForm
from .models import Session
from home.models import Notification
from offering.models import Timeslot
import decimal, pytz, datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from transaction.models import Transaction
from django.db.models.functions import Trunc
from django.db.models import Count, DateTimeField

TIMEZONELOCAL = pytz.timezone('Asia/Hong_Kong')

PRIVATE_TUTOR_TIMESLOTS = [(str(i) + ':00') for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [[str(i) + ':00', str(i) + ':30'] for i in range(8,22)]
CONTRACTED_TUTOR_TIMESLOTS = [item for sublist in CONTRACTED_TUTOR_TIMESLOTS for item in sublist]


@login_required
def search(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            univserity = form.cleaned_data.get('univserity')
            course = form.cleaned_data.get('course')
            name = form.cleaned_data.get('name')
            subject = form.cleaned_data.get('subject')
            identity = form.cleaned_data.get('identity')
            available_only = form.cleaned_data.get('available_only')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            '''start query'''
            allTutors = User.objects.filter(~Q(id=request.user.id) & (Q(profile__identity='T') | Q(profile__identity='C')))

            if identity == 'T':
                allTutors = allTutors.filter(profile__identity='T')
            elif identity == 'C':
                allTutors = allTutors.filter(profile__identity='C')

            if univserity != '0':
                allTutors = allTutors.filter(profile__school=univserity)
            if course != '':
                for tutor in allTutors:
                    tutor.profile.courses = tutor.profile.courses.split(';')
                    if course not in tutor.profile.courses:
                        allTutors = allTutors.exclude(id=tutor.id)
            if subject != '':
                for tutor in allTutors:
                    tutor.profile.subjects = tutor.profile.subjects.split(';')
                    if subject not in tutor.profile.subjects:
                        allTutors = allTutors.exclude(id=tutor.id)
            if name != '':
                name = name.split(' ')
                if len(name) == 1:
                    allTutors = allTutors.filter(Q(first_name=name[0]) | Q(last_name=name[0]))
                else:
                    allTutors = allTutors.filter((Q(first_name=name[0])&Q(last_name=name[1]))
                     | (Q(first_name=name[1])&Q(last_name=name[0])))
            if price_min != None:
                price_min = decimal.Decimal(price_min)
                allTutors = allTutors.filter(profile__price__gte=price_min)
            if price_max != None:
                price_max = decimal.Decimal(price_max)
                allTutors = allTutors.filter(profile__price__lte=price_max)
            if available_only == True:
                start_date = datetime.date.today()
                end_date = start_date + datetime.timedelta(days=7)
                maxtime = datetime.datetime(end_date.year, end_date.month, end_date.day, 22, 0, 0, 0)
                for tutor in allTutors:
                    available_timeslot = Timeslot.objects.filter(tutor__id=tutor.id, status='Available', start__lte=maxtime)
                    if len(available_timeslot) == 0:
                        allTutors = allTutors.exclude(id=tutor.id)
            for tutor in allTutors:
                    tutor.profile.subjects = tutor.profile.subjects.split(';')
            for tutor in allTutors:
                    tutor.profile.courses = tutor.profile.courses.split(';')
            return render(request, 'search.html', {'form': form, 'allTutors': allTutors})
    else:
        form = TutorForm()
    return render(request, 'search.html', {'form': form})

def booking(request, pk):
    # pk is a time slot ID
    timeslot = Timeslot.objects.get(pk=pk)
    timeslot.status = 'Booked'
    timeslot.save()

    session = Session(student=request.user, tutor=timeslot.tutor, start=timeslot.start, end=timeslot.end, status='Pending')
    session.save()

    name = session.tutor.get_full_name()

    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    startTime = timezone.localtime(session.start, timezonelocal)
    endTime = timezone.localtime(session.end, timezonelocal)

    dateStr = startTime.strftime('%Y-%m-%d')
    timeStr = startTime.strftime('%H:%M')  + ' ~ ' + endTime.strftime('%H:%M')

    tutor_price = session.tutor.profile.price
    commission = round(tutor_price *decimal.Decimal(0.05), 2)
    school = session.tutor.profile.getSchoolName()
    total_price = tutor_price + commission
    session_info = {'name': name, 'date':dateStr, 'time':timeStr, 'school': school, 'tutor_price': tutor_price, 'commission': commission}
    return render(request, 'confirmBooking.html', {'session_info': session_info, 'sessionID':sessionID})

def viewTutor(request, pk):
    currentTimeTruncDate = datetime.datetime.combine(timezone.now(), datetime.datetime.min.time()) 
    tomorrowTimeTruncDate = timezone.localtime(timezone.make_aware(currentTimeTruncDate, TIMEZONELOCAL) + datetime.timedelta(days = 1), TIMEZONELOCAL)
    nextWeekTimeTruncDate = timezone.localtime(timezone.make_aware(currentTimeTruncDate, TIMEZONELOCAL) + datetime.timedelta(days = 7), TIMEZONELOCAL)
    
    allSlots = Timeslot.objects.filter(tutor__id=pk, start__lte = nextWeekTimeTruncDate, start__gte = tomorrowTimeTruncDate).order_by('start')
    for slot in allSlots:
        startlocal = slot.start.astimezone(TIMEZONELOCAL)
        endlocal = slot.end.astimezone(TIMEZONELOCAL)
        date = startlocal.strftime('%b %d')
        startTime = startlocal.strftime('%H:%M')
        endTime = endlocal.strftime('%H:%M')

        slot_time_str = {'date':date, 'startTime':startTime, 'endTime':endTime}
        slot.slot_time_str = slot_time_str

    tutor = User.objects.get(id=pk)
    timeslots = PRIVATE_TUTOR_TIMESLOTS if tutor.profile.identity == 'T' else CONTRACTED_TUTOR_TIMESLOTS
    return render(request, 'tutor-info.html', {'allSlots': allSlots, 'timeslots': timeslots})


def confirmBooking(request, pk):
    session = Session.objects.get(pk=pk)
    price = round(session.tutor.profile.price*decimal.Decimal(1.05), 2)
    session_day_start = datetime.datetime(session.start.year, session.start.month, session.start.day, 0, 0, 0, 0)
    session_day_end = datetime.datetime(session.start.year, session.start.month, session.start.day, 23, 0, 0, 0)
    history = Session.objects.filter(start__gte=session_day_start, start__lte=session_day_end, status='Booked')
    check1 = False
    if len(history) == 0:
        check1 = True
    check2 = session.student.profile.wallet.checkBalance(price)
    status = 'successful'
    if check1 == True:
        if check2 == True:
            session.student.profile.wallet.withdraw(price)
            medium = User.objects.get(username='admin')
            medium.profile.wallet.addBalance(price)
            utcCurrentTime = timezone.now()
            timezonelocal = pytz.timezone('Asia/Hong_Kong')
            currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
            new_transaction = Transaction(from_wallet = session.student.profile.wallet, to_wallet = medium.profile.wallet, 
                time = currentTime, amount = price, description = 'Tutorial payment')
            new_transaction.save()
            session.status = 'Booked'
            session.save()
            Notification(session.student, 'Your session booking is successful, your have paid HK$' + str(price) + '.')
        else:
            timeslot = Timeslot.objects.filter(tutor=session.tutor, start=session.start, end=session.end, status='Booked')[0]
            timeslot.status = 'Available'
            timeslot.save()
            Notification(session.student, 'Your session booking is unsuccessful due to insufficient balance.')
            session.delete()
            status = 'unsuccessful'
        return render(request, 'confirmConfirmBooking.html', {'status': status})
    else:
        timeslot = Timeslot.objects.filter(tutor=session.tutor, start=session.start, end=session.end, status='Booked')[0]
        timeslot.status = 'Available'
        timeslot.save()
        session.delete()
        return render(request, 'samedayBooking.html', {'tutor_id': session.tutor.id})

def cancelConfirmBooking(request, pk):
    session = Session.objects.get(pk=pk)
    tutor_id = session.tutor.id
    timeslot = Timeslot.objects.filter(tutor=session.tutor, start=session.start, end=session.end, status='Booked')[0]
    timeslot.status = 'Available'
    timeslot.save()
    session.delete()
    return redirect('viewTutor', pk=tutor_id)

def canceling(request, pk):
    return render(request, 'confirmCanceling.html', {'sessionID':pk})

def confirmCanceling(request, pk):
    session = Session.objects.filter(pk=pk)[0]
    session.status = 'Canceled'
    session.save()
    timeslot = Timeslot.objects.filter(tutor=session.tutor, start=session.start, end=session.end, status='Booked')[0]
    timeslot.status = 'Available'
    timeslot.save()
    price = round(session.tutor.profile.price*decimal.Decimal(1.05), 2)
    session.student.profile.wallet.addBalance(price)
    medium = User.objects.get(username='admin')
    medium.profile.wallet.withdraw(price)
    utcCurrentTime = timezone.now()
    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
    new_transaction = Transaction(from_wallet = medium.profile.wallet, to_wallet = session.student.profile.wallet, 
        time = currentTime, amount = price, description = 'Tutorial payment')
    new_transaction.save()
    Notification(session.student, 'Your session has been canceled, a refund of HK$' + str(price) + ' has been added to your wallet.')
    return redirect('session')

def cancelConfirmCanceling(request):
    return redirect('session')

def session(request):
    allSessions = Session.objects.filter(student=request.user, status='Booked')
    return render(request, 'records.html', {'allSessions': allSessions, 'active':0})

def sessionHistory(request):
    allSessions = Session.objects.filter(Q(student=request.user) & ~Q(status='Booked'))
    return render(request, 'records.html', {'allSessions': allSessions, 'active':1})

def viewSession(request, pk):
    session_info = Session.objects.get(pk=pk)
    return render(request, 'viewSession.html', {'session':session_info, 'sessionID':pk})