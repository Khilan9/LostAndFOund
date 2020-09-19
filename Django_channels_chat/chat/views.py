from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def chatselect(request):
    return render(request,"chat/chatbutton.html")

def room(request, room_name='a'):
    return render(request, 'chat/room.html', {
        'room_name': 'a'
    })