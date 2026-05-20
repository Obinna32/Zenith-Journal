import calendar
from datetime import date, datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from .models import Entry
from .forms import EntryForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import openai
from django.utils import timezone
import os

# Create your views here.
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = ['date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['ai_summary'] = get_ai_summary(self.request.user)
        except Exception:
            context['ai_summary'] = "AI Reflection currently unavailable."
        return context
class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entry_form.html'
    success_url = reverse_lazy('entry-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'entries/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = date.today()
        month = int(self.request.GET.get('month', today.month))
        year = int(self.request.GET.get('year', today.year))        

        cal = calendar.Calendar(firstweekday=6) # Start on Sunday
        month_days = cal.monthdatescalendar(year, month)
        
        user_entries = Entry.objects.filter(
            user=self.request.user, 
            date_created__year=year, 
            date_created__month=month
        ).values_list('date_created', flat=True)

        first_day_of_month = date(year, month, 1)
        prev_month = first_day_of_month - timedelta(days=1)
        next_month = first_day_of_month + timedelta(days=32)

        context['month_days'] = month_days
        context['current_month'] = first_day_of_month
        context['prev_month'] = prev_month
        context['next_month'] = next_month
        context['user_entry_dates'] = user_entries
        return context

def export_journal_pdf(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date_created')

    template_path = 'entries/pdf_export.html'
    context = {'entries':entries, 'user':request.user}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="my_journal.pdf'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html+ '</pre>')
    return response

def get_ai_summary(user):
    last_week = timezone.now() - timedelta(days=7)
    entries = Entry.objects.filter(user=user, date_created__gte=last_week)

    if entries.count() < 3:
        return "Write at least 3 entries this week to get an AI Insights"
    
    combined_text = ""
    for entry in entries:
        combined_text += f"Date: {entry.date_created} - Mood: {entry.mood}\nContent: {entry.content}\n\n"

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful life coach. Analyze the following journal entries and provide a 3-sentence summary of the user's week and one piece of encouragement."},
            {"role": "user", "content": combined_text}
        ]
    )
    return response.choices[0].message.content

