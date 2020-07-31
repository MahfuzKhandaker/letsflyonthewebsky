from django import template
from pages.models import About

register = template.Library()


@register.inclusion_tag('pages/_about_me.html')
def about_me():
    about_instance = About.objects.all()
    return {'about_instance': about_instance}
