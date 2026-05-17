from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entry(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊 Happy'),
        ('neutral', '😐 Neutral'),
        ('sad', '😔 Sad'),
        ('stressed', '😫 Stressed'),
        ('productive', '🔥 Productive'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_created = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        return f"{self.title} - {self.date_created}"