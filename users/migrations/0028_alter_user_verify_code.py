# Generated by Django 4.2.2 on 2024-10-12 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_user_verify_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verify_code',
            field=models.CharField(default='310597', max_length=6, verbose_name='Код верификации'),
        ),
    ]
