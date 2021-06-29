# Generated by Django 3.2.3 on 2021-06-29 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_type_block_components'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record_components',
            options={'ordering': ['-id'], 'verbose_name': 'Учет', 'verbose_name_plural': 'Учет компонентов'},
        ),
        migrations.AlterField(
            model_name='record_block',
            name='status',
            field=models.CharField(blank=True, choices=[('ожидает', 'ожидает'), ('готов', 'готов'), ('отправлен', 'отправлен'), ('неисправен', 'неисправен'), ('производитель', 'производитель')], default='ожидает', max_length=15, null=True, verbose_name='Состояние'),
        ),
        migrations.AlterField(
            model_name='record_components',
            name='component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record_component', related_query_name='query_record_compoent', to='base.components', verbose_name='Компонент'),
        ),
    ]
