# Generated by Django 3.2.3 on 2022-02-10 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_maker_maker_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maker',
            old_name='date_add',
            new_name='date_add_maker',
        ),
        migrations.RenameField(
            model_name='maker',
            old_name='date_shipment',
            new_name='date_shipment_maker',
        ),
    ]
