# Generated by Django 3.1.4 on 2020-12-13 23:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0005_auto_20201213_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payee',
            name='AccountNumber',
        ),
        migrations.RemoveField(
            model_name='payee',
            name='FirstName',
        ),
        migrations.RemoveField(
            model_name='payee',
            name='LastName',
        ),
        migrations.RemoveField(
            model_name='payee',
            name='SortCode',
        ),
        migrations.AddField(
            model_name='payee',
            name='PayeeID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
