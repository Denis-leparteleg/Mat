# Generated by Django 3.2.9 on 2022-01-10 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='busid',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='nos',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='userid',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bus',
            name='nos',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bus',
            name='price',
            field=models.SlugField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bus',
            name='rem',
            field=models.SlugField(max_length=255),
        ),
    ]
