from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    #function calling by views.index
    
    path('',views.home,name='home'),
    path('webmainpage',views.webmainpage, name='webmainpage'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('newuser',views.newuser,name='newuser'),
    path('checklogin',views.checklogin,name="checklogin"),
    path('lostform',views.lostform,name="lostform"),
    path('foundform',views.foundform,name='foundform'),
    path('showlost',views.showlost,name='showlost'),
    path('showfound',views.showfound,name='showfound'),
    path('storelost',views.storelost,name='storelost'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('searchlost',views.searchlost,name='searchlost'),
    path('searchfound',views.searchfound,name='searchfound'),
    path('update',views.update,name='update'),
    path('deletelost/<int:id>',views.deletelost,name='deletelost'),
    path('deletefound/<int:id>',views.deletefound,name='deletefound'),
    path('showlostreward',views.showlostreward,name='showlostreward'),
    path('claim',views.claim,name='claim'),
    path('searchclaim',views.searchclaim,name='searchclaim'),
    path('storeclaim/<int:foundid>',views.storeclaim,name='storeclaim'),
    path('showclaim',views.showclaim,name='showclaim'),
    path('returned/<int:foundid>',views.returned,name='returned'),
    path('returned1',views.returned1,name='returned1'),
    path('showreturn',views.showreturn,name='showreturn'),
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('showmatching',views.showmatching,name='showmatching'),
    path('rtnform',views.rtnform,name='rtnform'),
    path('searchreturn',views.searchreturn,name='searchreturn'),
    path('storereturn/<int:lostid>',views.storereturn,name='storereturn'),
    path('recieved/<int:lostid>',views.recieved,name='recieved'),
    path('recieved1',views.recieved1,name='recieved1'),
    #Added
    path('chat/', views.room, name='index'),
    #path('storefound',views.storefound,name='storefound')
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
