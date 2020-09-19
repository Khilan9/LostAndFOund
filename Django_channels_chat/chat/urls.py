from django.urls import path

from . import views

app_name='chat'

urlpatterns = [
    #path('', views.index, name='index'),
    path('',views.chatselect,name='chatselect'),
    path('chat/', views.room, name='index'),
    path('chat/<room_name>/', views.room, name='room'),
]