# Generated by Django 4.2.2 on 2024-10-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0011_habit_next_notification_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='periodicity',
            field=models.CharField(choices=[('1 day', 'Каждый 1 день'), ('2 days', 'Каждые 2 дня'), ('3 days', 'Каждые 3 дня'), ('4 days', 'Каждые 4 дня'), ('5 days', 'Каждые 5 дней'), ('6 days', 'Каждые 6 дней'), ('7 days', 'Каждые 7 дней')], default='1', help_text='Повторять...', max_length=50, verbose_name='Периодичность'),
        ),
    ]
