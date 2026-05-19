from django.urls import path
from .views import EntryListView, EntryCreateView, CalendarView

urlpatterns = [
    path('', EntryListView.as_view(), name='entry-list'),
    path('new/', EntryCreateView.as_view(), name='entry-create'),
    path("calendar/", CalendarView.as_view(), name="calendar")
]

