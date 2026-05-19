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

# Create your views here.
class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "entries/entry_list.html"
    context_object_name = "entries"
    ordering = ['date_created']

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('-date_created')

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