# Generated by Django 3.2.3 on 2022-03-03 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_auto_20220303_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maker',
            name='note_maker',
            field=models.CharField(blank=True, max_length=65, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]
