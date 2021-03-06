from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import BookingForm, TutorForm, ReviewForm
from .models import Session, Review
from home.models import Notification
from offering.models import Timeslot
import decimal, pytz, datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from transaction.models import Transaction, Coupon
from django.db.models.functions import Trunc
from django.db.models import Count, DateTimeField, Avg
from django.http import JsonResponse

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
            tutortype = form.cleaned_data.get('tutortype')
            available_only = form.cleaned_data.get('available_only')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            '''start query'''
            allTutors = User.objects.filter(~Q(id=request.user.id) & Q(profile__identity='T') & Q(tutorprofile__show_profile=1))
            if tutortype== 'P':
                allTutors = allTutors.filter(tutorprofile__tutortype='P')
            elif tutortype == 'C':
                allTutors = allTutors.filter(tutorprofile__tutortype='C')
            if univserity != '0' and univserity != '':
                allTutors = allTutors.filter(profile__school=univserity)
            if course != '':
                for tutor in allTutors:
                    tutor.tutorprofile.courses = tutor.tutorprofile.courses.lower().split(';')
                    cor = course.lower().split(';')
                    for each in cor:
                        if each not in tutor.tutorprofile.courses:
                            allTutors = allTutors.exclude(id=tutor.id)
            if subject != '':
                for tutor in allTutors:
                    tutor.tutorprofile.subjects = tutor.tutorprofile.subjects.lower().split(';')
                    sub = subject.lower().split(';')
                    for each in sub:
                        if each not in tutor.tutorprofile.subjects:
                            allTutors = allTutors.exclude(id=tutor.id)
            if name != '':
                name = name.lower().split(' ')
                if len(name) == 1:
                    allTutors = allTutors.filter(Q(first_name__icontains=name[0]) | Q(last_name__icontains=name[0]))
                else:
                    allTutors = allTutors.filter((Q(first_name__icontains=name[0])|Q(last_name__icontains=name[1]))
                     | (Q(first_name__icontains=name[1])|Q(last_name__icontains=name[0])))
            if price_min != None:
                price_min = decimal.Decimal(price_min)
                allTutors = allTutors.filter(tutorprofile__price__gte=price_min)
            if price_max != None:
                price_max = decimal.Decimal(price_max)
                allTutors = allTutors.filter(tutorprofile__price__lte=price_max)
            if available_only:
                start_date = datetime.date.today()
                end_date = start_date + datetime.timedelta(days=7)
                maxtime = datetime.datetime(end_date.year, end_date.month, end_date.day, 22, 0, 0, 0)
                for tutor in allTutors:
                    currentTimeTruncDate = datetime.datetime.combine(timezone.now(), datetime.datetime.min.time()) 
                    tomorrowTimeTruncDate = timezone.localtime(timezone.make_aware(currentTimeTruncDate, TIMEZONELOCAL) + datetime.timedelta(days = 1), TIMEZONELOCAL)
                    available_timeslot = Timeslot.objects.filter(tutor__id=tutor.id, status='Available', start__gte = tomorrowTimeTruncDate, start__lte=maxtime)
                    if len(available_timeslot) == 0:
                        allTutors = allTutors.exclude(id=tutor.id)
            for tutor in allTutors:
                    tutor.tutorprofile.subjects = tutor.tutorprofile.subjects.split(';')
            for tutor in allTutors:
                    tutor.tutorprofile.courses = tutor.tutorprofile.courses.split(';')

            return render(request, 'search.html', {'form': form, 'allTutors': allTutors})
    else:
        form = TutorForm()
    return render(request, 'search.html', {'form': form})

@login_required
def viewTutor(request, pk):
    currentTimeTruncDate = datetime.datetime.combine(timezone.now(), datetime.datetime.min.time()) 
    tomorrowTimeTruncDate = timezone.localtime(timezone.make_aware(currentTimeTruncDate, TIMEZONELOCAL) + datetime.timedelta(days = 1), TIMEZONELOCAL)
    nextWeekTimeTruncDate = timezone.localtime(timezone.make_aware(currentTimeTruncDate, TIMEZONELOCAL) + datetime.timedelta(days = 7), TIMEZONELOCAL)

    avaliable_next_week = len(Timeslot.objects.filter(tutor__id=pk, start__lte = nextWeekTimeTruncDate, start__gte = tomorrowTimeTruncDate, status='Available').order_by('start'))

    allSlots = None

    if avaliable_next_week != 0:
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
    tutor.tutorprofile.courses = tutor.tutorprofile.courses.split(';')
    tutor.tutorprofile.subjects = tutor.tutorprofile.subjects.split(';')

    times = PRIVATE_TUTOR_TIMESLOTS if tutor.tutorprofile.tutortype == 'P' else CONTRACTED_TUTOR_TIMESLOTS
    return render(request, 'tutor-info.html', {'allSlots': allSlots, 'timeslots': times, 'tutor': tutor})

@login_required
def booking(request, pk):
    # pk is a time slot ID
    
    timeslot = Timeslot.objects.get(pk=pk)
    if timeslot.status == "Available":
        timeslot.status = 'Booked'
        timeslot.save()

        session = Session(student=request.user, timeslot=timeslot, status='Pending')
        session.save()

        name = timeslot.tutor.get_full_name()

        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        startTime = timezone.localtime(timeslot.start, timezonelocal)
        endTime = timezone.localtime(timeslot.end, timezonelocal)

        dateStr = startTime.strftime('%Y-%m-%d')
        timeStr = startTime.strftime('%H:%M')  + ' ~ ' + endTime.strftime('%H:%M')

        tutor_price = timeslot.tutor.tutorprofile.price
        tutor_type = timeslot.tutor.tutorprofile.tutortype
        commission = round(tutor_price *decimal.Decimal(0.05), 2)
        school = timeslot.tutor.profile.get_school_name()
        total_price = tutor_price + commission
        session_info = {'name': name, 'date':dateStr, 'time':timeStr, 'school': school, 'tutor_price': tutor_price, 'tutor_type': tutor_type, 'total_price': total_price, 'commission': commission}
        return render(request, 'confirmBooking.html', {'session_info': session_info, 'sessionID':session.id})
    else:
        button = {'label':'Go to home page', 'link': '/'}
        return_msg = {'success': False, 'msg': 'Error', 'reason': "Illegal request.", 'button': button}
    
        return render(request, 'nav-result.html', {'return_msg': return_msg})

@login_required
def continueBooking(request, pk):

    session = Session.objects.get(pk=pk)
    timeslot = session.timeslot

    name = timeslot.tutor.get_full_name()

    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    startTime = timezone.localtime(timeslot.start, timezonelocal)
    endTime = timezone.localtime(timeslot.end, timezonelocal)

    dateStr = startTime.strftime('%Y-%m-%d')
    timeStr = startTime.strftime('%H:%M')  + ' ~ ' + endTime.strftime('%H:%M')

    tutor_price = timeslot.tutor.tutorprofile.price
    tutor_type = timeslot.tutor.tutorprofile.tutortype
    commission = round(tutor_price *decimal.Decimal(0.05), 2)
    school = timeslot.tutor.profile.get_school_name()
    total_price = tutor_price + commission
    session_info = {'name': name, 'date':dateStr, 'time':timeStr, 'school': school, 'tutor_price': tutor_price, 'tutor_type': tutor_type, 'total_price': total_price, 'commission': commission}
    return render(request, 'confirmBooking.html', {'session_info': session_info, 'sessionID':session.id})

@login_required
def confirmBooking(request, pk):
    session = Session.objects.get(pk=pk)
    session_day_start = datetime.datetime(session.timeslot.start.year, session.timeslot.start.month, session.timeslot.start.day, 0, 0, 0, 0)
    session_day_end = datetime.datetime(session.timeslot.start.year, session.timeslot.start.month, session.timeslot.start.day, 23, 0, 0, 0)
    sameTutorHistory = Session.objects.filter(student=request.user, timeslot__tutor=session.timeslot.tutor, timeslot__start__gte=session_day_start, timeslot__start__lte=session_day_end, status='Booked')
    check1 = False
    if len(sameTutorHistory) == 0:
        check1 = True
    if check1:
        timeClashBookedSession = Session.objects.filter(Q(student=request.user) & ~Q(timeslot__tutor=session.timeslot.tutor) & 
            (Q(timeslot__start=session.timeslot.start) | Q(timeslot__end=session.timeslot.end)) & Q(status='Booked'))
        check2 = False
        return_msg = {'success': False, 'msg': ''}
        if len(timeClashBookedSession) == 0:
            check2 = True
        if check2:
            timeClashSelf = Timeslot.objects.filter(Q(tutor=request.user) & (Q(start=session.timeslot.start) | Q(end=session.timeslot.end)) & 
                (Q(status='Booked') | Q(status='Available')))
            check_self = False
            if len(timeClashSelf) == 0:
                check_self = True
            if check_self:
                session.commission = round(session.timeslot.tutor.tutorprofile.price*decimal.Decimal(0.05), 2)
                price = session.timeslot.tutor.tutorprofile.price + session.commission

                if request.method == 'POST':
                    coupon_code = request.POST.get('coupon', None)
                    check2_5 = Coupon.isValid(coupon_code)
                    if check2_5:
                        session.commission = 0
                        price = session.timeslot.tutor.tutorprofile.price

                check3 = session.student.profile.wallet.checkBalance(price)
                
                if check3:
                    session.student.profile.wallet.withdraw(price)
                    medium = User.objects.get(username='admin')
                    medium.profile.wallet.addBalance(price)
                    utcCurrentTime = timezone.now()
                    timezonelocal = pytz.timezone('Asia/Hong_Kong')
                    currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
                    new_transaction = Transaction(from_wallet = session.student.profile.wallet, to_wallet = medium.profile.wallet, 
                        time = currentTime, amount = price, description = 'Tutorial payment')
                    new_transaction.save()
                    session.transaction0 = new_transaction
                    session.status = 'Booked'
                    session.save()
                    Notification(session.student, 'Your session booking on ' + 
                        session.timeslot.start.astimezone(TIMEZONELOCAL).strftime('%Y-%m-%d %H:%M') + ' ~ ' + session.timeslot.end.astimezone(TIMEZONELOCAL).strftime('%H:%M') + ' is successful, your have paid HK$' + str(price) + '.')
                    Notification(session.timeslot.tutor, 'Your time slot is booked, a new session has been scheduled on ' + 
                        session.timeslot.start.astimezone(TIMEZONELOCAL).strftime('%Y-%m-%d %H:%M') + ' ~ ' + session.timeslot.end.astimezone(TIMEZONELOCAL).strftime('%H:%M') + '.')
                    return_msg = {'success': True,  'msg': 'Booking Successfully Placed'}
                else:
                    session.timeslot.status = 'Available'
                    session.timeslot.save()
                    Notification(session.student, 'Your session booking is unsuccessful due to insufficient balance.')
                    session.delete()
                    button = {'label':'Go to my wallet', 'link': '/wallet/'}
                    return_msg = {'success': False, 'msg': 'Booking Unsuccessful', 'reason': 'Insufficient balance in your wallet', 'button': button}
            else:
                session.timeslot.status = 'Available'
                session.timeslot.save()
                tutor_id = session.timeslot.tutor.id
                session.delete()
                button = {'label':'Go back to browse other timeslots', 'link': '/viewTutor/' + str(tutor_id)}
                return_msg = {'success': False, 'msg': 'Booking Unsuccessful', 'reason': "A time clash with your teaching time.", 'button': button}
        else:
            session.timeslot.status = 'Available'
            session.timeslot.save()
            tutor_id = session.timeslot.tutor.id
            session.delete()
            button = {'label':'Go back to browse other timeslots', 'link': '/viewTutor/' + str(tutor_id)}
            return_msg = {'success': False, 'msg': 'Booking Unsuccessful', 'reason': "A time clash with your previously booked sessions occurs.", 'button': button}
    else:
        session.timeslot.status = 'Available'
        session.timeslot.save()
        tutor_id = session.timeslot.tutor.id
        session.delete()
        button = {'label':'Go back to browse other timeslots', 'link': '/viewTutor/' + str(tutor_id)}
        return_msg = {'success': False, 'msg': 'Booking Unsuccessful', 'reason': "You can't book more than one sessions of the same tutor on the same day.", 'button': button}
    
    return render(request, 'nav-result.html', {'return_msg': return_msg})

@login_required
def cancelConfirmBooking(request, pk):
    session = Session.objects.get(pk=pk)
    session.timeslot.status = 'Available'
    session.timeslot.save()
    tutor_id = session.timeslot.tutor.id
    session.delete()
    return redirect('viewTutor', pk=tutor_id)

@login_required
def canceling(request, pk):
    session = Session.objects.filter(pk=pk)[0]
    session.status = 'Canceled'
    session.timeslot.status = 'Available'
    session.timeslot.save()
    price = session.transaction0.amount
    session.student.profile.wallet.addBalance(price)
    medium = User.objects.get(username='admin')
    medium.profile.wallet.withdraw(price)
    utcCurrentTime = timezone.now()
    timezonelocal = pytz.timezone('Asia/Hong_Kong')
    currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
    new_transaction = Transaction(from_wallet = medium.profile.wallet, to_wallet = session.student.profile.wallet, 
        time = currentTime, amount = price, description = 'Tutorial payment')
    new_transaction.save()
    session.transaction1 = new_transaction
    session.save()
    Notification(session.student, 'Your session on ' + 
        session.timeslot.start.astimezone(TIMEZONELOCAL).strftime('%Y-%m-%d %H:%M') + ' ~ ' + session.timeslot.end.astimezone(TIMEZONELOCAL).strftime('%H:%M') + ' has been canceled, a refund of HK$' + str(price) + ' has been added to your wallet.')
    return redirect('session')

@login_required
def session(request):
    allSessions = Session.objects.filter(
        Q(student=request.user) & (Q(status='Booked') | Q(status='Pending') | Q(status='Committed')))
    return render(request, 'records.html', {'allSessions': allSessions, 'active':0})

@login_required
def sessionHistory(request):
    allSessions = Session.objects.filter(
        Q(student=request.user) & ~Q(status='Booked') & ~Q(status='Pending') & ~Q(status='Committed'))
    return render(request, 'records.html', {'allSessions': allSessions, 'active':1})

@login_required
def sessionTutoring(request):
    allSessions = Session.objects.filter(timeslot__tutor=request.user, status='Booked')
    return render(request, 'recordsTutoring.html', {'allSessions': allSessions, 'active':0})

@login_required
def sessionTutoringHistory(request):
    allSessions = Session.objects.filter(Q(timeslot__tutor=request.user) & ~Q(status='Booked'))
    return render(request, 'recordsTutoring.html', {'allSessions': allSessions, 'active': 1})

@login_required
def viewSession(request, pk):
    session = Session.objects.get(pk=pk)
    payment = session.transaction0.amount
    commission = session.commission
    reviews = Review.objects.filter(session = session)

    review = None
    form = None
    if session.status == 'Ended' and session.student == request.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                score = form.cleaned_data.get('score')
                comment = form.cleaned_data.get('comment')
                isAnonymous = form.cleaned_data.get('isAnonymous')

                utcCurrentTime = timezone.now()
                timezonelocal = pytz.timezone('Asia/Hong_Kong')
                currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
                
                new_review = Review(session = session, score = score, time = currentTime, comment = comment, isAnonymous = isAnonymous)
                new_review.save()

                session.status = 'Reviewed'
                session.save()

                review = new_review

        form = ReviewForm()
    elif session.status == 'Reviewed' and session.student == request.user:
        review = Review.objects.get(session = session)
    return render(request, 'session-info.html', {'session':session, 'sessionID':pk, 'payment':payment, 'commission':commission, 'form':form, 'review':review, 'user':request.user})

@login_required
def getAllReviewFormatted(request, pk):
    user = User.objects.get(id = pk)
    all_reviews = user.tutorprofile.get_all_reviews()
    formatted_list_reviews = [{'author': review.session.student.get_full_name() if not review.isAnonymous else 'Anonymous User', 
        'avatar': '/' + review.session.student.profile.picture.url if not review.isAnonymous else '/static/assets/img/avatar/def_avatar.png',
        'score': review.score, 'comment': review.comment} for review in all_reviews]
    # print(formatted_list_reviews)
    return JsonResponse({'reviews': formatted_list_reviews})