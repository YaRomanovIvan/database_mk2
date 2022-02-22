import csv
import os

from django.core.management.base import BaseCommand

from base.models import Unit
from database.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "unique_region.csv")


class Command(BaseCommand):
    help = "Load unique block name"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH) as file:
            reader = csv.reader(file)
            for row in reader:
                Unit.objects.get_or_create(region=row[0])