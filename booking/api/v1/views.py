from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from booking.models import Member, Inventory, Booking
from booking.api.v1.serializers import BookingSerializer

MAX_BOOKINGS = 2


class BookItemView(APIView):
    """
    View for handling booking operations.
    Methods:
    post(request): Handles the creation of a new booking for a member.
        - Validates the presence of member_id and inventory_id in the request data.
        - Ensures the member has not exceeded the maximum booking limit.
        - Checks the availability of the inventory item.
        - Creates a new booking and decrements the inventory count atomically.
        - Returns the created booking data with a 201 status code or an error message with a 400 status code.

    get(request): Retrieves bookings for a specific member or all bookings.
        - Accepts an optional member_id query parameter.
        - Returns serialized booking data with a 200 status code.
    """

    def post(self, request):
        member_id = request.data.get('member_id')
        inventory_id = request.data.get('inventory_id')

        if not all([member_id, inventory_id]):
            return Response({'error': 'Member ID and Inventory ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        member = get_object_or_404(Member, id=member_id)
        inventory = get_object_or_404(Inventory, id=inventory_id)

        if Booking.objects.filter(member=member).count() >= MAX_BOOKINGS:
            return Response({'error': 'Max booking limit reached'}, status=status.HTTP_400_BAD_REQUEST)

        if inventory.remaining_count <= 0:
            return Response({'error': 'No items left in inventory'}, status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(member=member, inventory=inventory)

        Inventory.objects.filter(id=inventory.id).update(
            remaining_count=F('remaining_count') - 1)

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        member_id = request.query_params.get('member_id')

        if member_id:
            bookings = Booking.objects.filter(member_id=member_id)
        else:
            bookings = Booking.objects.all()

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelBookingView(APIView):
    """
    Handles the cancellation of a booking.
    This view processes POST requests to cancel a booking by its ID. It requires
    a 'booking_id' in the request data. If the booking ID is not provided, it
    returns a 400 Bad Request response. Upon successful cancellation, it
    atomically increments the inventory's remaining count and deletes the
    booking, returning a 200 OK response with a success message.
    """

    def post(self, request):
        booking_id = request.data.get('booking_id')

        if not booking_id:
            return Response({'error': 'Booking ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        booking = get_object_or_404(Booking, id=booking_id)
        inventory = booking.inventory

        # Atomically increment inventory count and delete booking
        Inventory.objects.filter(id=inventory.id).update(
            remaining_count=F('remaining_count') + 1)
        booking.delete()

        return Response({'message': 'Booking cancelled'}, status=status.HTTP_200_OK)
