# Generated by Django 4.0.10 on 2024-04-03 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_customcreation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customcreation',
            old_name='total_charge',
            new_name='cost',
        ),
    ]