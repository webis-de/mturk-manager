from django import template
import json

register = template.Library()

@register.simple_tag
def get_count_distinct_parameters(json_dict_parameters):
	dict_parameters = json.loads(json_dict_parameters)
	return len(dict_parameters)