from django.urls import path
from booking.api.v1.views import BookItemView, CancelBookingView

urlpatterns = [
    path('book/', BookItemView.as_view(), name='book_item'),
    path('booking/', BookItemView.as_view(), name='booking_list'),
    path('booking/<int:member_id>', BookItemView.as_view(), name='booking_list'),
    path('cancel/', CancelBookingView.as_view(), name='cancel_booking'),
]
