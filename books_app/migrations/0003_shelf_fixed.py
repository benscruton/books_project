# Generated by Django 2.2.4 on 2021-03-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0002_book_isbn'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='fixed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]