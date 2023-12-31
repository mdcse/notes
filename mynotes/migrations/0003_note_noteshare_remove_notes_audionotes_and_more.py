# Generated by Django 4.2.2 on 2023-06-21 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mynotes', '0002_remove_audionotes_notes_remove_audionotes_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('type', models.CharField(choices=[('text', 'Text'), ('audio', 'Audio'), ('video', 'Video')], max_length=10)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='audio/')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='video/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoteShare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mynotes.note')),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='notes',
            name='audionotes',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='user',
        ),
        migrations.RemoveField(
            model_name='notes',
            name='videonotes',
        ),
        migrations.DeleteModel(
            name='AudioNotes',
        ),
        migrations.DeleteModel(
            name='Notes',
        ),
        migrations.DeleteModel(
            name='VideoNotes',
        ),
    ]
