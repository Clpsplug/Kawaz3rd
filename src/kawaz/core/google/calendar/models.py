# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .conf import settings
from .utils import get_model
from .backend import get_backend


class GoogleCalendarBridge(models.Model):
    """
    A bridge model which enable Google Calendar Sync with Event like model
    """
    event = models.OneToOneField(settings.GOOGLE_CALENDAR_EVENT_MODEL,
                                 primary_key=True)
    gcal_event_id = models.CharField(_("Google Calendar Event ID"),
                                     default='', editable=False,
                                     blank=True, max_length=128)


def get_event_model():
    """
    Get an event model class from settings.GCAL_EVENT_MODEL
    """
    return get_model(settings.GOOGLE_CALENDAR_EVENT_MODEL)


@receiver(post_save)
def update_google_calendar(sender, instance, created, **kwargs):
    model = get_event_model()
    if sender == model:
        backend = get_backend()
        backend.update(instance)


@receiver(post_delete)
def delete_google_calendar(sender, instance, **kwargs):
    model = get_event_model()
    if sender == model:
        backend = get_backend()
        backend.delete(instance)
