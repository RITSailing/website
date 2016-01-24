from django import forms
from django.conf import settings
from flatpages.models import FlatPage
from django.utils.translation import ugettext, ugettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class FlatpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
        help_text=_("Example: '/about/contact/'. Make sure to have leading"
                    " and trailing slashes."),
        error_messages={
            "invalid": _("This value must contain only letters, numbers,"
                         " dots, underscores, dashes, slashes or tildes."),
        },
    )
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = FlatPage
        fields = '__all__'

    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('/'):
            raise forms.ValidationError(
                ugettext("URL is missing a leading slash."),
                code='missing_leading_slash',
            )
        if (settings.APPEND_SLASH and
                'django.middleware.common.CommonMiddleware' in settings.MIDDLEWARE_CLASSES and
                not url.endswith('/')):
            raise forms.ValidationError(
                ugettext("URL is missing a trailing slash."),
                code='missing_trailing_slash',
            )
        return url

    def clean(self):
        url = self.cleaned_data.get('url')

        same_url = FlatPage.objects.filter(url=url)
        if self.instance.pk:
            same_url = same_url.exclude(pk=self.instance.pk)

        return super(FlatpageForm, self).clean()
