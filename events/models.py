from __future__ import unicode_literals
from django.db import models
from main.models import TeamMember

class Event(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    closed_rsvp = models.BooleanField(default=False, help_text="Whether or not to let members RSVP themselves. Used mostly for regattas.")
    going = models.ManyToManyField(TeamMember, blank=True)
    def __str__(self):
        return self.title
    def get_month(self):
        if self.end_date and self.start_date.month != self.end_date.month:
            return self.start_date.strftime("%b") + " - " + self.end_date.strftime("%b")
        return self.start_date.strftime("%b")
    def get_day(self):
        if self.end_date and self.start_date.day != self.end_date.day:
            return self.start_date.strftime("%d") + " - " + self.end_date.strftime("%d")
        return self.start_date.strftime("%d")
