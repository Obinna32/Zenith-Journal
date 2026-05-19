from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
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
    content = CKEditor5Field('Text', config_name='default')
    date_created = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')

    habits_completed = models.ManyToManyField(Habit, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        return f"{self.title} - {self.date_created}"