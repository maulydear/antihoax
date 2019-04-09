# Generated by Django 2.1.7 on 2019-04-08 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20190408_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='staff status'),
        ),
    ]