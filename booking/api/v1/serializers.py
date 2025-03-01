from rest_framework import serializers
from ...models import Member, Inventory, Booking


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Member model, converting model instances to JSON and vice versa.
    Includes all fields of the Member model.
    """
    class Meta:
        model = Member
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Inventory model, converting model instances to JSON 
    and validating data for creating or updating Inventory objects.
    """
    class Meta:
        model = Inventory
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model, converting model instances to JSON 
    and validating incoming data for creating or updating bookings.
    """
    class Meta:
        model = Booking
        fields = '__all__'
