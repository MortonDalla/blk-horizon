# Generated by Django 3.0.6 on 2020-07-02 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200702_2241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
    ]
