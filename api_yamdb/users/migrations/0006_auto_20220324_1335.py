# Generated by Django 2.2.16 on 2022-03-24 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220324_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='', max_length=255),
        ),
    ]
