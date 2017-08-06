from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Device(models.Model):
    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=200)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

class Command(models.Model):
    device = models.ForeignKey('willy.Device', related_name='commands')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=2000, default="")

    def __str__(self):
        return self.name

class Event(models.Model):
    device = models.ForeignKey('willy.Device', related_name = 'device_events')
    command = models.ForeignKey('willy.Command', related_name = 'command_events')
    scheduled_time = models.DateTimeField(default=timezone.now)
    everyday = models.BooleanField(default=False)

    class Meta:
        ordering = ['scheduled_time']

