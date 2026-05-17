from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Entry
from .forms import EntryForm

# Create your views here.
class EntryListView(ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = ['date_created']

class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    success_url = reverse_lazy('entry-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)