import csv
from msilib import type_key
import os

from django.core.management.base import BaseCommand

from base.models import Record_block, Maker, Type_block, Maker_company
from database.settings import BASE_DIR

CSV_FILE_PATH = os.path.join(BASE_DIR, "express_maker.csv")


class Command(BaseCommand):
    help = "Load send maker"

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH) as file:
            reader = csv.reader(file)
            for row in reader:
                row = row[0].split(';')
                block = Record_block.objects.get(number_block=int(row[0]))
                type_block = Type_block.objects.get(name_block=block.name_block)
                maker = Maker_company.objects.get(name='ЭКСПРЕСС')
                if not type_block.maker:
                    type_block.maker = maker
                    type_block.save()
                print('--------------------')
                print(row)
                print(type_block.maker)
                print('--------------------')
                if not row[1] and row[2]:
                    if block.status == 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_add_maker=row[2],
                            maker_status='забракован',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif not row[2] and row[1]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_add_maker=row[2],
                            maker_status='отправлен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif block.status != 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_add_maker=row[2],
                            maker_status='возвращен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    else:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_add_maker=row[2],
                            maker_status='ожидает',
                            reason=row[4],
                            note_maker=row[5]
                        )
                elif not row[2] and row[1]:
                    if block.status == 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            maker_status='забракован',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif not row[2] and row[1]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            maker_status='отправлен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif block.status != 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            maker_status='возвращен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    else:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            maker_status='ожидает',
                            reason=row[4],
                            note_maker=row[5]
                        )
                elif row[1] and row[2]:
                    if block.status == 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            date_add_maker=row[2],
                            maker_status='забракован',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif not row[2] and row[1]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            date_add_maker=row[2],
                            maker_status='отправлен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif block.status != 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            date_add_maker=row[2],
                            maker_status='возвращен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    else:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            date_shipment_maker=row[1],
                            date_add_maker=row[2],
                            maker_status='ожидает',
                            reason=row[4],
                            note_maker=row[5]
                        )
                else:
                    if block.status == 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            maker_status='забракован',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif not row[2] and row[1]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            maker_status='отправлен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    elif block.status != 'неисправен' and row[2]:
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            maker_status='возвращен',
                            reason=row[4],
                            note_maker=row[5]
                        )
                    else:
                        print('НЕТ ДАТЫ И ВРЕМЕНИ')
                        Maker.objects.get_or_create(
                            block=block,
                            number_block=block.number_block,
                            name_block=block.name_block,
                            serial_number=block.serial_number,
                            maker=maker,
                            maker_status='ожидает',
                            reason=row[4],
                            note_maker=row[5]
                        )