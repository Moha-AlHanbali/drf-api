from django.db import models
from rest_framework import serializers
from .models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'title', 'band', 'rating','description', 'author', 'created', 'updated')