# Generated by Django 3.1.4 on 2020-12-12 22:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20201211_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='TransactionTime',
            field=models.CharField(default=datetime.datetime(2020, 12, 12, 22, 45, 16, 814445, tzinfo=utc), max_length=50),
        ),
    ]