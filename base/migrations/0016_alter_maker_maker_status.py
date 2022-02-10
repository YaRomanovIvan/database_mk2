# Generated by Django 3.2.3 on 2022-02-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20220210_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maker',
            name='maker_status',
            field=models.CharField(choices=[('возвращен', 'возвращен'), ('отправлен', 'отправлен'), ('забракован', 'забракован')], default='отправлен', max_length=15, verbose_name='Состояние'),
        ),
    ]
