from django import template
from django.utils.html import format_html, escape
import json

register = template.Library()

@register.simple_tag
def get_count_distinct_parameters(json_dict_parameters):
	dict_parameters = json.loads(json_dict_parameters)
	return len(dict_parameters)

@register.simple_tag()
def render_info(tpl):
	html = '''
		<a class="fas fa-info-circle" title="{}" data-content="{}" data-type="info" tabindex="1"></a>
	'''.format(tpl[0], escape(tpl[1]))

	return format_html(html)