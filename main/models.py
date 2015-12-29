from django.db import models
from django.contrib.auth.models import AbstractUser

# class TeamMember(AbstractUser):
#     YEAR_LEVELS = (
#             ('1', '1st'),
#             ('2', '2nd'),
#             ('3', '3rd'),
#             ('4', '4th'),
#             ('5', '5th'),
#             ('0', 'Other'),
#     )
#
#     SAILING_LEVELS = (
#             ('1', 'Beginner'),
#             ('2', 'Intermediate'),
#             ('3', 'Race'),
#     )
#     year_level = models.CharField(max_length = 1, choices=YEAR_LEVELS)
#     sailing_level = models.CharField(max_length = 1, choices=SAILING_LEVELS)
#     board_pos = models.CharField(max_length = 50)
#     avatar = models.URLField()
