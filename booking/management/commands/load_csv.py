from datetime import datetime
from django.utils.timezone import make_aware
from django.core.management.base import BaseCommand

import pandas as pd

from booking.models import Inventory, Member


class Command(BaseCommand):
    """
    Command to load members and inventory data from CSV files into the database.
    This command reads data from 'members.csv' and 'inventory.csv' files, converts
    necessary fields to appropriate formats, and bulk creates Member and Inventory
    objects in the database. It provides feedback on the number of records loaded
    or if no records were found.
"""
    help = "Load members and inventory from CSV files"

    def handle(self, *args, **kwargs):
        self.load_members()
        self.load_inventory()

    def load_members(self):
        df = pd.read_csv('members.csv')

        members = []
        for _, row in df.iterrows():
            naive_datetime = datetime.strptime(
                row['date_joined'], "%Y-%m-%dT%H:%M:%S")
            aware_datetime = make_aware(naive_datetime)

            members.append(Member(
                name=row['name'],
                surname=row['surname'],
                booking_count=row['booking_count'],
                date_joined=aware_datetime
            ))

        if members:
            Member.objects.bulk_create(members, ignore_conflicts=False)
            self.stdout.write(self.style.SUCCESS(
                f'Loaded {len(members)} members'))
        else:
            self.stdout.write(self.style.WARNING(
                "No members found to import."))

    def load_inventory(self):
        df = pd.read_csv('inventory.csv')
        items = [
            Inventory(
                title=row['title'],
                description=row['description'],
                remaining_count=row['remaining_count'],
                expiration_date=datetime.strptime(
                    row['expiration_date'], "%d/%m/%Y").date()
            )
            for _, row in df.iterrows()
        ]
        Inventory.objects.bulk_create(items, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(
            f'Loaded {len(items)} inventory items'))
