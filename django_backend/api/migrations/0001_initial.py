# Generated by Django 4.2.1 on 2023-05-20 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='project', max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(choices=[(5, 'Vital'), (4, 'Urgent'), (3, 'Important'), (2, 'Can Wait'), (1, 'Minor')])),
                ('completion_status', models.CharField(choices=[('TODO', 'TODO'), ('INPROGRESS', 'INPROGRESS'), ('ONHOLD', 'ONHOLD'), ('RESOLVED', 'RESOLVED')], default='TODO', max_length=64)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.project')),
            ],
        ),
    ]
