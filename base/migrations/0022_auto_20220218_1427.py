# Generated by Django 3.2.3 on 2022-02-18 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20220218_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер счета'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.CharField(blank=True, max_length=180, null=True, verbose_name='ФИО'),
        ),
    ]
