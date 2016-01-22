from __future__ import unicode_literals

from django.db import models
from main.models import TeamMember
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    author = models.ForeignKey(TeamMember)
    header_image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=True)
    pinned_post = models.BooleanField(default=False)
    content = RichTextUploadingField()
    def __str__(self):
        return self.title
