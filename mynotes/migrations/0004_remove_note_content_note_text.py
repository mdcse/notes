# Generated by Django 4.2.2 on 2023-06-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynotes', '0003_note_noteshare_remove_notes_audionotes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='content',
        ),
        migrations.AddField(
            model_name='note',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
