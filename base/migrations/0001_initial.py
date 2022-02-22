import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('type_component', models.CharField(max_length=100, verbose_name='Тип компонента')),
                ('marking', models.CharField(max_length=100, unique=True, verbose_name='Маркировка')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
                ('amount_eis', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество ЭИС')),
                ('amount_trk', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество ТРК')),
                ('amount_vts', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество ВТС')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена/шт')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компоненты',
                'ordering': ['type_component'],
            },
        ),
        migrations.CreateModel(
            name='Defect_statement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('date_add', models.DateField(verbose_name='Дата')),
                ('defect_1', models.CharField(max_length=100, verbose_name='Неисправность 1')),
                ('defect_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Неисправность 2')),
                ('defect_3', models.CharField(blank=True, max_length=100, null=True, verbose_name='Неисправность 3')),
                ('result', models.CharField(max_length=100, verbose_name='Заключение')),
            ],
            options={
                'verbose_name': 'Деектная ведомость',
                'verbose_name_plural': 'Дефектные ведомости',
                'ordering': ['block'],
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата учета')),
                ('date_shipment', models.DateField(blank=True, null=True, verbose_name='Дата отправки')),
                ('date_add', models.DateField(blank=True, null=True, verbose_name='Дата приёма')),
                ('note', models.CharField(blank=True, max_length=65, null=True, verbose_name='Примечание')),
            ],
            options={
                'verbose_name': 'Ремон производителя',
                'verbose_name_plural': 'Ремонты Производителей',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Maker_company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Производитель',
                'verbose_name_plural': 'Производители',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_processing', models.DateField(auto_now_add=True, verbose_name='Дата обработки заявки')),
                ('date_order', models.DateField(verbose_name='Дата заказа')),
                ('date_receipt', models.DateField(blank=True, null=True, verbose_name='Дата получения')),
                ('invoice_number', models.CharField(max_length=100, verbose_name='Номер счета')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Record_block',
            fields=[
                ('number_block', models.IntegerField(primary_key=True, serialize=False, verbose_name='Номер блока')),
                ('serial_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Заводской_номер')),
                ('date_add', models.DateField(auto_now_add=True, verbose_name='Дата приема')),
                ('date_repair', models.DateField(blank=True, null=True, verbose_name='Дата ремонта')),
                ('date_shipment', models.DateField(blank=True, null=True, verbose_name='Дата отправки')),
                ('FIO', models.CharField(blank=True, max_length=30, null=True, verbose_name='ФИО')),
                ('status', models.CharField(blank=True, choices=[('ожидает', 'ожидает'), ('готов', 'готов'), ('отправлен', 'отправлен'), ('неисправен', 'неисправен'), ('производитель', 'производитель')], default='ожидает', max_length=15, null=True, verbose_name='Состояние')),
                ('note', models.CharField(blank=True, max_length=200, null=True, verbose_name='Примечание')),
                ('passed', models.CharField(blank=True, max_length=25, null=True, verbose_name='Передан ФИО')),
            ],
            options={
                'verbose_name': 'Блок в центре',
                'verbose_name_plural': 'Блоки в центре',
                'ordering': ['-number_block'],
            },
        ),
        migrations.CreateModel(
            name='Record_component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=10, null=True, verbose_name='Компания')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('date_add', models.DateField(auto_now_add=True, verbose_name='Дата учета')),
            ],
            options={
                'verbose_name': 'Учет',
                'verbose_name_plural': 'Учет компонентов',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50, unique=True, verbose_name='Подразделение')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
                'ordering': ['region'],
            },
        ),
        migrations.CreateModel(
            name='Type_block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_block', models.CharField(max_length=100, unique=True, verbose_name='Наименование блока')),
                ('components', models.ManyToManyField(blank=True, related_name='block_components', to='base.Component', verbose_name='Компоненты блока')),
                ('maker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_maker', to='base.maker_company', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Тип блока',
                'verbose_name_plural': 'Типы блоков',
                'ordering': ['name_block'],
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(verbose_name='Количество')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата заявки')),
                ('status', models.CharField(choices=[('ожидает', 'ожидает'), ('обработан', 'обработан'), ('получен', 'получен')], default='ожидает', max_length=25, null=True, verbose_name='Статус заявки')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Примечание')),
                ('component', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='component_request', to='base.component', verbose_name='Наименование компонента')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-pk'],
            },
        ),
    ]
