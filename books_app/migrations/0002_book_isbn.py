# Generated by Django 2.2.4 on 2021-03-03 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ISBN',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
