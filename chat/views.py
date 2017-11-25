from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from .models import Chat
from django.contrib.auth.models import User
import pytz, datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def chat(request, name):
    c = Chat.objects.filter((Q(user_from=request.user) & Q(user_to__username=name)) | (Q(user_from__username=name) & Q(user_to=request.user))).order_by('-time')
    return render(request, "chat.html", {'chat': c, 'user_to_name': name})

@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        name = request.POST.get('receiver_name', None)
        receiver = User.objects.get(username=name)
        utcCurrentTime = timezone.now()
        timezonelocal = pytz.timezone('Asia/Hong_Kong')
        currentTime = timezone.localtime(utcCurrentTime, timezonelocal)
        c = Chat(user_from=request.user, user_to=receiver, message=msg, time=currentTime)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user_from.username })
    else:
        return HttpResponse('Request must be POST.')

@login_required
def Messages(request, name):
    receiver = User.objects.filter(username=name)
    if len(receiver) != 0:
        c = Chat.objects.filter((Q(user_from=request.user)&Q(user_to=receiver)) | (Q(user_to=request.user)&Q(user_from=receiver))).order_by('-time')
    else:
        c = Chat.objects.none()
    return render(request, 'messages.html', {'chat': c})