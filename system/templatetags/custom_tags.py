
from django import template

register = template.Library()
def returnImageURLOrEmpty(value,image):
    if(image):
        return image.url
    else:
        return ""
register.filter('returnImageURLOrEmpty', returnImageURLOrEmpty)