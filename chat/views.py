from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from .models import Chat
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required
def chat(request, name):
    c = Chat.objects.filter(user_from=request.user, user_to__username=name)
    return render(request, "chat.html", {'chat': c, 'user_to_name': name})
@login_required
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        name = request.POST.get('receiver_name', None)
        receiver = User.objects.get(username=name)
        c = Chat(user_from=request.user, user_to=receiver, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user_from.username })
    else:
        return HttpResponse('Request must be POST.')
@login_required
def Messages(request):
    c = Chat.objects.filter(Q(user_from=request.user) | Q(user_to=request.user))
    return render(request, 'messages.html', {'chat': c})