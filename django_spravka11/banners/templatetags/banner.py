from banners.models import Banner, BannerGroup
from django import template
from django.template import Context, Template
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def banner_group(context, group, tpl='group.html'):
	try:
		group = BannerGroup.objects.get(slug=str(group))
		banners = Banner.objects.filter(public=True, group=group)
	except:
		banners = False
		group = False
	if(banners and group):
		context['banners'] = banners
		context['group'] = group

	t = template.loader.get_template(tpl)
	return t.render(template.Context(context))

@register.simple_tag(takes_context=True)
def banner_one(context, banner_id, tpl='banner.html'):
	try:
		banner = Banner.objects.get(id=banner_id, public=True)
	except:
		banner = False

	context['banner'] = banner

	t = template.loader.get_template(tpl)
	return t.render(template.Context(context))

# block render
@register.simple_tag(takes_context=True)
def render(context, content):
	try:
		tpl = Template(content)
		content = Context(context)
		return tpl.render(content)
	except:
		return 'Render Error'