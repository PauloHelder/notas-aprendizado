# Generated by Django 5.1.4 on 2024-12-11 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learnings', '0006_rename_owner_id_topic_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='owner',
        ),
    ]
