from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.sessions.models import Session

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def chatselect(request):
    return render(request,"chat/chatbutton.html")

def room(request, room_name='a'):
    request.session['sessionuserid']=request.POST['id']
    request.session['sessionusernme']=request.POST['username']
    print(request.session['sessionuserid'])
    print(request.session['sessionusernme'])
    return render(request, 'chat/room.html', {
        'room_name': 'a',
        'username': mark_safe(json.dumps(request.session['sessionusernme'])),
        'idofuser': mark_safe(json.dumps(request.session['sessionuserid'])),
    })