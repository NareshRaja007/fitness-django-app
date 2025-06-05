from django.urls import path
from .views import ClassListView, BookingView, BookingListView

urlpatterns = [
    path('classes', ClassListView.as_view()),
    path('book', BookingView.as_view()),
    path('bookings', BookingListView.as_view()),
]