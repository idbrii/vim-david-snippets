import os
import re
import vim

def _search_and_return_first_group_from_regex_before_current_line(regex):
    w = vim.current.window
    row, col = w.cursor
    for line in reversed(vim.current.window.buffer[:row]):
        match = regex.match(line)
        if match:
            return match.groups()
    return None, None

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

def has_access_to_unityobject():
    static_line, method = _search_and_return_first_group_from_regex_before_current_line(re.compile("^.*?(static)?\s+(\S+\s+[A-Z]\S+)\(.*\)\s*$"))
    if static_line:
        return False
    parent = get_cs_parentclass()
    if parent:
        valid_this = ['MonoBehaviour', 'ScriptableObject']
        return any([p_class in parent for p_class in valid_this])
    return False


def guess_namespace(hint=None):
    top = vim.eval('g:snips_company')
    if hint:
        folder = hint
    else:
        folder = os.path.basename(os.path.dirname(vim.current.buffer.name))
    return "{top}.{folder}".format(top=top, folder=folder)

