import re

def _search_and_return_first_group_from_regex(regex, snip):
    for line in snip.buffer:
        match = regex.match(line)
        if match:
            return match.group(1)
    return None

def get_cs_classname(snip):
    return _search_and_return_first_group_from_regex(re.compile(".*class (\w*)"), snip)

def get_cs_parentclass(snip):
    return _search_and_return_first_group_from_regex(re.compile(".*class \w+ : (\w+)"), snip)

def is_parent_class_unityobject(snip):
    parent = get_cs_parentclass(snip)
    if parent:
        valid_this = ['MonoBehaviour', 'ScriptableObject']
        return any([p_class in parent for p_class in valid_this])
    return False
