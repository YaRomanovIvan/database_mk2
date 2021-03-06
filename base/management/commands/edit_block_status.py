from django.core.management.base import BaseCommand
from base.models import Record_block


class Command(BaseCommand):
    help = "Load defect record block"

    def handle(self, *args, **options):
        wait = "принят"
        ship = "выдан"
        red = "забракован"
        maker = "производителю"
        qs = Record_block.objects.all()
        print('----------------------------')
        print('Ожидайте...')
        print('----------------------------')
        for get in qs:
            if get.number_block == 93318:
                break
            if get.status == 'отправлен':
                get.status = ship
            elif get.status == 'ожидает':
                get.status = wait
            elif get.status == 'производитель':
                get.status = maker
            elif get.status == 'неисправен':
                get.status = red
            print(get.number_block)
            get.save()
        print('----------------------------')
        print('Конец')
        print('----------------------------')
