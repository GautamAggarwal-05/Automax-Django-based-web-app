from django.forms import widgets
from django.utils.html import format_html

class CustomPhotoImageFieldWidget(widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        default_html = super().render(name, value, attrs, **kwargs)
        image_url = getattr(value, 'url', None)

        if not image_url:
            return default_html

        image_html = format_html(
            '<img src="{}" width="200" alt="Current profile photo">',
            image_url,
        )
        return format_html('{}{}', image_html, default_html)