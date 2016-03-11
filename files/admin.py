from django.contrib import admin
from .models import File, Folder

class ItemAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("slug", )
        form = super(ItemAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register(File, ItemAdmin)
admin.site.register(Folder, ItemAdmin)
