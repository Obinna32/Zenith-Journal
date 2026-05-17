from django.shortcuts import render
from django.views.generic import ListView
from .models import Entry

# Create your views here.
class EntryListView(ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = ['date_created']