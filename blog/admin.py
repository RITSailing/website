from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from models import Post
from main.models import TeamMember

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        self.fields['author'].queryset = TeamMember.objects.filter(user__is_staff=True)
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'author', 'date', 'pinned_post',)
    list_filter = ('pinned_post',)
    search_fields = ('title','author', 'date', )

admin.site.register(Post, PostAdmin)
