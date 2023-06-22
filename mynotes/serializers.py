from rest_framework import serializers
from .models import Notes


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ('email', 'title', 'text', 'audio', 'video')
        read_only_fields = ('audio', 'video')


