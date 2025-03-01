from django.db import models


class Member(models.Model):
    """
    Represents a member with personal details and booking information.

    """

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    booking_count = models.IntegerField(default=0)
    date_joined = models.DateTimeField()

    def __str__(self):
        return f"{self.name} {self.surname}"


class Inventory(models.Model):
    """
    Represents an inventory item with details such as title, description, 
    remaining count, and expiration date.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    remaining_count = models.PositiveIntegerField()
    expiration_date = models.DateField()

    def __str__(self):
        return self.title


class Booking(models.Model):
    """
    Represents a booking record linking a member to an inventory item,
    including the date of booking.
    """
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name} booked {self.inventory.title}"
