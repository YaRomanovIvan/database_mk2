# Generated by Django 3.2.3 on 2022-02-10 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20210922_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maker',
            name='date',
        ),
        migrations.RemoveField(
            model_name='maker',
            name='maker',
        ),
        migrations.AlterField(
            model_name='maker',
            name='date_add',
            field=models.DateField(blank=True, null=True, verbose_name='Дата возврата'),
        ),
        migrations.AlterField(
            model_name='maker',
            name='date_shipment',
            field=models.DateField(blank=True, null=True, verbose_name='Дата отправки производителю'),
        ),
    ]
