from django.db import models
from django.contrib.auth.models import User
from calendar import monthrange
from datetime import datetime, timedelta

class MemberManager(models.Manager):
    def create_member(self, user):
        try:
            return self.get(user=user)
        except Exception as e:
            return self.create(user=user)

YEAR_LEVELS = [
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', 'Other'),
]

SAILING_LEVELS = (
        ('1', 'Beginner'),
        ('2', 'Intermediate'),
        ('3', 'Race'),
)
class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year_level = models.CharField(max_length = 1, choices=YEAR_LEVELS, default="1")
    sailing_level = models.CharField(max_length = 1, choices=SAILING_LEVELS, default="1")
    eboard_pos = models.CharField(max_length = 50, blank=True)
    dues_paid = models.DateField(blank=True, null=True)
    avatar = models.URLField(blank=True)
    objects = MemberManager()
    def is_dues_paid(self):
        return self.dues_paid and monthdelta(datetime.date.today(), self.dues_paid) < 6
    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

def monthdelta(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta

class RequestManager(models.Manager):
    def create_request(self, email, first_name, last_name, year_level):
        return self.create(email=email, first_name=first_name, last_name=last_name, year_level=year_level)

class Request(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    year_level = models.CharField(max_length = 1, choices=YEAR_LEVELS, default="1")
    accepted = models.BooleanField(default=False)
    was_checked = models.BooleanField(default=False, editable=False)
    objects = RequestManager()
    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
    def save(self, **kwargs):
        if self.accepted and not self.was_checked:
            # TODO Email person to tell them they were accepted
            self.was_checked = True
        elif not self.accepted and self.was_checked:
            # Fired on uncheck if needed later on
            self.was_checked = False
        super(Request, self).save(kwargs)
