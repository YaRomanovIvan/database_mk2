# Generated by Django 3.2.3 on 2022-02-10 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_maker_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maker',
            name='maker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.maker_company', verbose_name='Производитель'),
        ),
    ]
