# Generated by Django 3.1.4 on 2020-12-14 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201212_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='sort_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
