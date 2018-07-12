from django import template
from PIL import Image, ImageDraw

register = template.Library()


@register.simple_tag
def img(i, d):
	im = Image.open('app/static/img/image.jpg', 'r')

	pix = im.getpixel((d,i))
	return str(pix)
