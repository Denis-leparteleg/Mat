# Generated by Django 3.2.9 on 2022-01-11 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mat', '0006_accesstoken_booking_mat_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='phone_number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='number',
        ),
    ]
