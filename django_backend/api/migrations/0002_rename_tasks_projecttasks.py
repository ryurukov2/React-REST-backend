# Generated by Django 4.2.1 on 2023-05-20 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tasks',
            new_name='ProjectTasks',
        ),
    ]
