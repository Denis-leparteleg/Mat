# Generated by Django 3.2.9 on 2022-01-11 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mat', '0003_auto_20220110_1525'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
        migrations.AlterField(
            model_name='book',
            name='nos',
            field=models.DecimalField(decimal_places=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('B', 'Booked'), ('C', 'Cancelled')], default='B', max_length=255),
        ),
    ]