from django.db import models

# Create your models here.
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