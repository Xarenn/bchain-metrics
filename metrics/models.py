from datetime import timezone

from django.db import models

from rest_framework import serializers


class Block(models.Model):
    name = models.CharField('Event Name', max_length=120,default='')
    event_date = models.DateTimeField('Event Date',default='')
    venue = models.CharField(max_length=120, default='')
    manager = models.CharField(max_length = 60, default='')
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('name',)
