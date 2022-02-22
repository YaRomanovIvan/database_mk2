import csv
import os

from django.core.management.base import BaseCommand

from base.models import Record_block, Maker
from database.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "elsiel_maker.csv")


class Command(BaseCommand):
    help = "Load send maker"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH) as file:
            reader = csv.reader(file)
            for row in reader:
                row = row[0].split(';')
                block = Record_block.objects.get(number_block=int(row[0]))
                print(row[0])
                if row[3] == 'возвращен':
                    Maker.objects.get_or_create(
                        block=block,
                        number_block=block.number_block,
                        name_block=block.name_block,
                        serial_number=block.serial_number,
                        maker=block.name_block.maker,
                        date_shipment_maker=row[1],
                        date_add_maker=row[2],
                        maker_status='возвращен',
                        reason=row[4],
                        note_maker=row[5]
                    )
                elif row[3] == 'забракован':
                    Maker.objects.get_or_create(
                        block=block,
                        number_block=block.number_block,
                        name_block=block.name_block,
                        serial_number=block.serial_number,
                        maker=block.name_block.maker,
                        date_shipment_maker=row[1],
                        date_add_maker=row[2],
                        maker_status='забракован',
                        reason=row[4],
                        note_maker=row[5]
                    )