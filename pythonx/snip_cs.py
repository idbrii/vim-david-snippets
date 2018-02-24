import re
import vim

def _search_and_return_first_group_from_regex(regex):
    for line in vim.current.window.buffer:
        match = regex.match(line)
        if match:
            return match.group(1)
    return None

def get_cs_classname():
    return _search_and_return_first_group_from_regex(re.compile(".*class (\w*)"))

def get_cs_parentclass():
    return _search_and_return_first_group_from_regex(re.compile(".*class \w+ : (\w+)"))

def is_parent_class_unityobject():
    parent = get_cs_parentclass()
    if parent:
        valid_this = ['MonoBehaviour', 'ScriptableObject']
        return any([p_class in parent for p_class in valid_this])
    return False
