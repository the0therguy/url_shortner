# Generated by Django 4.0.7 on 2022-09-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_shortner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='expiration_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]