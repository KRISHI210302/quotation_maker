# Generated by Django 4.0.10 on 2024-04-06 02:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0008_rename_total_charge_customcreation_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customcreation',
            old_name='cost',
            new_name='total_charge',
        ),
    ]
