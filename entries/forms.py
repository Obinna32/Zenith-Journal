from django import forms
from .models import Entry, Habit

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'date_created', 'mood', 'content', 'habits_completed']

        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Title of your day...'}),
            'mood': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows':5}),
            'habits_completed': forms.CheckboxSelectMultiple(),
        }