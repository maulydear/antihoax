# Generated by Django 2.1.7 on 2019-04-08 11:03

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20190408_1749'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.models.CustomUserManager()),
            ],
        ),
    ]
