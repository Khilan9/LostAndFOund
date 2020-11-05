from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
# Create your models here.

#Model for Register NewUser 
class Newuser(models.Model):
    userid = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=40)
    phoneno = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    class Meta():
        db_table = "newuser"

#Store lost item database
class Storelost(models.Model):
    selectitem=models.CharField(max_length=20)
    color=models.CharField(max_length=15)
    brand=models.CharField(max_length=20)
    place=models.CharField(max_length=10)
    date=models.DateField()
    description=models.CharField(max_length=100)
    useridforeign=models.ForeignKey(Newuser,on_delete=models.CASCADE,blank=True)
    ownername=models.CharField(max_length=10,blank=True)
    reward=models.IntegerField(default=0,blank=True)
    #Recieved or not
    recievedstatus=models.IntegerField(default=0,blank=True)

    lostbranchname=models.CharField(max_length=20,blank=True)
    class Meta():
        db_table="storelost"

class Storefound(models.Model):
    selectitem=models.CharField(max_length=20)
    color=models.CharField(max_length=15)
    brand=models.CharField(max_length=20)
    place=models.CharField(max_length=10)
    date=models.DateField()
    img=models.ImageField(upload_to='pics/')
    description=models.CharField(max_length=100)
    useridforeignfound=models.ForeignKey(Newuser,on_delete=models.CASCADE,blank=True)
    foundername=models.CharField(max_length=10,blank=True)
    #By admin if many days no one make claim
    markasnotclaim=models.BooleanField(default=False,blank=True)
    
    returnedstatus=models.IntegerField(default=0,blank=True)

    handovername=models.CharField(max_length=20,blank=True)

    branchname=models.CharField(max_length=20,blank=True)
    
    #Save image by resize so display same at webpage
    def save(self, ** kwargs):
            #Opening the uploaded image
            im = Image.open(self.img)
            output = BytesIO()
            #Resize/modify the image
            im = im.resize((200,200))

            #after modifications, save it to the output
            im.save(output, format='JPEG', quality=100)
            output.seek(0)

            #change the imagefield value to be the newley modifed image value
            self.img = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.img.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

            super(Storefound,self).save()
    class Meta():
        db_table="storefound"

class Storeclaim(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=10)
    date=models.DateField()
    foundername=models.CharField(max_length=10)
    claimername=models.CharField(max_length=10)
    claimerid=models.ForeignKey(Newuser,on_delete=models.CASCADE,blank=True)
    founditemid=models.ForeignKey(Storefound,on_delete=models.CASCADE,blank=True)
    givenstatus=models.IntegerField(default=0,blank=True)
    
    class Meta():
        db_table = "storeclaim"

class Storematching(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=10)
    date=models.DateField()
    lostitemid=models.ForeignKey(Storelost,on_delete=models.CASCADE,blank=True)
    founditemid=models.ForeignKey(Storefound,on_delete=models.CASCADE,blank=True)
    
    class Meta():
        db_table="storematching"


class Storereturn(models.Model):
    name=models.CharField(max_length=20)
    place=models.CharField(max_length=10)
    date=models.DateField()
    ownername=models.CharField(max_length=10)
    foundername=models.CharField(max_length=10)
    founderid=models.ForeignKey(Newuser,on_delete=models.CASCADE,blank=True)
    lostitemid=models.ForeignKey(Storelost,on_delete=models.CASCADE,blank=True)
    givenstatus=models.IntegerField(default=0,blank=True)

    class Meta():
        db_table="storereturn"


class Chat(models.Model):
    useridforeignchat=models.ForeignKey(Newuser,on_delete=models.CASCADE,blank=True)
    chatmessage=models.CharField(max_length=500)
    class Meta():
        db_table="chat"

class Message(models.Model):
    idofuser=models.CharField(max_length=20)
    content=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta():
        db_table="message"

    def __str__(self):
        return self.idofuser

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()

    