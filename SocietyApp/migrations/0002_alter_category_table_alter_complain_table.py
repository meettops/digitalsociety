# Generated by Django 4.0.4 on 2022-05-27 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocietyApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='Category',
        ),
        migrations.AlterModelTable(
            name='complain',
            table='Complain',
        ),
    ]