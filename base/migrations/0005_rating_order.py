# Generated by Django 4.0.4 on 2022-06-02 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_remove_rating_book_isbn_remove_rating_user_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rating', models.IntegerField(max_length=2)),
                ('book_isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_s', models.DateTimeField()),
                ('date_e', models.DateField()),
                ('confirmed', models.BooleanField(default=False)),
                ('book_isbn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
