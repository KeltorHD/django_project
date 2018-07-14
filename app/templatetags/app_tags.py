from django import template
from PIL import Image, ImageDraw

register = template.Library()


@register.simple_tag
def img(pk, i, d):
	im = Image.open('app/static/img/{}.jpg'.format(pk), 'r')

	pix = im.getpixel((d,i))
	return str(pix)
