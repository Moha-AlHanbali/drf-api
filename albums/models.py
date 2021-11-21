from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey


class Album(models.Model):
    title = models.CharField(max_length = 64)
    band = models.CharField(max_length = 64)
    rating = IntegerField()
    description = models.TextField()
    author = ForeignKey(get_user_model(), on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title


