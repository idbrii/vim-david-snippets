#! /usr/bin/env python

import re

def __convert_enum_to_case(enum_type, enum_value_text):
    enum_value_text = re.sub('(,.*)?\s*$', ':', enum_value_text)
    case = []
    case.append((1, "case {t}.{v}".format(t=enum_type, v=enum_value_text)))
    case.append((2, "break;"))
    case.append((2, ""))
    return case

def last_token(text):
    """
    last_token(str, object) -> str

    >>> last_token("enum class Actions")
    'Actions'
    """
    i = text.rfind(" ")
    if i > -1:
        return text[i+1:]
    return None


def convert_enum_to_switch(enum_value_textblock):
    """
    convert_enum_to_switch(str, object) -> str

    >>> enum_text = '''
    ... public enum Actions
    ... {
    ...     Idle,
    ...     Grab,
    ...     Place,
    ...     Throw,
    ... }
    ... '''
    >>> enum_text_cpp = '''enum class Actions
    ... {
    ...     Idle,
    ...     Grab,
    ...     Place,
    ...     Throw
    ... };
    ... '''
    >>> for pair in convert_enum_to_switch(enum_text_cpp):
    ...     print(("    " * pair[0]) + pair[1])
        case Actions.Idle:
            break;
    <BLANKLINE>
        case Actions.Grab:
            break;
    <BLANKLINE>
        case Actions.Place:
            break;
    <BLANKLINE>
        case Actions.Throw:
            break;
    <BLANKLINE>
    """
    enum_value_lines = enum_value_textblock.split('\n')
    enum_value_lines = [line.strip() for line in enum_value_lines if re.search("[{}]", line) is None]
    enum_value_lines = [line for line in enum_value_lines if len(line) > 0]
    enum_type = last_token(enum_value_lines[0])
    if enum_type:
        enum_value_lines = enum_value_lines[1:] # skip typename
    else:
        enum_type = "EnumType"
    enum_value_lines = [line.strip() for line in enum_value_lines if re.search(line, "[{}]") is None]
    case_pairs = [__convert_enum_to_case(enum_type, case) for case in enum_value_lines]
    case_lines = []
    for a in case_pairs[:-1]:
        case_lines.extend(a)
    return case_lines




def _test():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    _test()
