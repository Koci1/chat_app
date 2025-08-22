from django.db import models

# Create your models here.

class Message(models.Model):

    """
    Model poruke koja ce se pohranjivati u bazu
    """
    owner = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.content
