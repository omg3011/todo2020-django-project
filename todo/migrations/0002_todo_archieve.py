# Generated by Django 3.1.4 on 2020-12-27 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='archieve',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
