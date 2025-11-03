from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch 


class ConverstaionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('participants',queryset=User.objects.only('id','username'))
        )
    
class Conservation(models.Model):
    participants = models.ManyToManyField(User,related_name='conservations')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ConverstaionManager()

    def __str__(self):
        return "Conversation with : " + " , ".join([user.username for user in self.participants.all()])

class Message (models.Model):
    converstaion = models.ForeignKey(Conservation,on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    content = models.TextField()
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} in {self.content[:20]}"
    