# Generated by Django 3.2.9 on 2022-01-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mat', '0010_auto_20220111_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mat',
            name='sacco_name',
            field=models.TextField(max_length=30),
        ),
    ]
