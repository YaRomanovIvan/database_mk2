# Generated by Django 3.2.3 on 2022-03-03 07:58

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_merge_0022_auto_20220218_1427_0026_auto_20220222_1108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': [django.db.models.expressions.OrderBy(django.db.models.expressions.F('date_processing'), descending=True, nulls_first=True), 'provider', 'date_created', 'invoice_number'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_time',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Срок поставки'),
        ),
        migrations.AlterField(
            model_name='maker',
            name='note_maker',
            field=models.TextField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]
