from __future__ import unicode_literals

from django.db import models
from main.models import TeamMember
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    author = models.ForeignKey(TeamMember)
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    content = RichTextUploadingField()
    def __str__(self):
        return self.title
