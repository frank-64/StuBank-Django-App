# Generated by Django 3.1.4 on 2020-12-30 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.RemoveField(
            model_name='message',
            name='seen',
        ),
    ]