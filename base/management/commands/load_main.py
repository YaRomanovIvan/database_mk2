from base64 import encode
import csv
import os

from django.core.management.base import BaseCommand

from base.models import Record_block, Type_block, Unit
from database.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "baseTRKUTF8.csv")


class Command(BaseCommand):
    help = "Load record block"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                row = row[0].split(';')
                if Record_block.objects.filter(pk=int(row[0])):
                    print('Блок уже в списке')
                else:
                    if row[1] == '"Пожарная сигнализация УПС ""Дельта-М"""':
                        name_block = Type_block.objects.get(name_block='Пожарная сигнализация УПС "Дельта-М"')
                    else:
                        name_block = Type_block.objects.get(name_block=row[1])
                    print('Добавлен:')
                    print(row)
                    region = Unit.objects.get(region=row[6])
                    id_ = int(row[0])
                    if row[3] and row[4] and row[5]:
                        Record_block.objects.get_or_create(
                            number_block=id_,
                            name_block=name_block,
                            serial_number=row[2],
                            region=region,
                            date_add=row[3],
                            FIO='admin',
                            date_repair=row[4],
                            date_shipment=row[5],
                            status='выдан',
                            note=row[7],
                            passed='Старые записи',
                        )
                    elif row[3] and row[4] and not row[5]:
                        Record_block.objects.get_or_create(
                            number_block=id_,
                            name_block=name_block,
                            serial_number=row[2],
                            region=region,
                            date_add=row[3],
                            FIO='admin',
                            date_repair=row[4],
                            status='готов',
                            note=row[7],
                            passed='Старые записи',
                        )
                    elif row[3] and not row[4] and not row[5]:
                        Record_block.objects.get_or_create(
                            number_block=id_,
                            name_block=name_block,
                            serial_number=row[2],
                            region=region,
                            date_add=row[3],
                            FIO='admin',
                            status='принят',
                            note=row[7],
                            passed='Старые записи',
                        )