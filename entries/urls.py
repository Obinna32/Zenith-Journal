from django.urls import path
from .views import EntryListView, EntryCreateView

urlpatterns = [
    path('', EntryListView.as_view(), name='entry-list'),
    path('new/', EntryCreateView.as_view(), name='entry-create'),
]

