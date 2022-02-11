import csv
import os

from django.core.management.base import BaseCommand

from base.models import Type_block
from database.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "unique_block_name.csv")


class Command(BaseCommand):
    help = "Load unique block name"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH) as file:
            reader = csv.reader(file)
            for row in reader:
                name = row
                Type_block.objects.get_or_create(name_block=name[0])