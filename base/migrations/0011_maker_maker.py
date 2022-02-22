# Generated by Django 3.2.3 on 2022-02-10 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20220210_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='maker',
            name='maker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.maker_company', verbose_name='Производитель'),
            preserve_default=False,
        ),
    ]
