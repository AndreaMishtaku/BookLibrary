# Generated by Django 4.0.4 on 2022-06-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_order_date_s'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_author',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_title',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='book',
            name='image_url',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=100),
        ),
    ]