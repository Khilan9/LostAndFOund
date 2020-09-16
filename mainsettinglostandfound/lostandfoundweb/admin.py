from django.contrib import admin
from .models import Newuser,Storelost,Storefound
# Register your models here.

admin.site.register(Newuser)
admin.site.register(Storelost)
admin.site.register(Storefound)