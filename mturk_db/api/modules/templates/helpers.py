import re
from collections import Counter


def count_parameters_in_template(template: str):
    list_matches = re.findall('\$\{([a-zA-Z0-9_-]+)\}', template)
    counter = Counter(list_matches)
    return counter
