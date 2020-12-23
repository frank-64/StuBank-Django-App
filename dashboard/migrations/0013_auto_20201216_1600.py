# Generated by Django 3.1.4 on 2020-12-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20201216_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='Amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Category',
            field=models.CharField(choices=[('Dining Out', 'Dining Out'), ('Food Shopping', 'Food Shopping'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment'), ('Technology', 'Technology'), ('Clothing', 'Clothing'), ('Rent', 'Rent'), ('Healthcare', 'Healthcare'), ('Other', 'Other')], max_length=20),
        ),
    ]