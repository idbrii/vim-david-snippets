#! /usr/bin/env python

import re

def __convert_enum_to_case(enum_type, enum_value_text):
    enum_value_text = re.sub('(\s*=[^,]*)?(,.*)?\s*$', ':', enum_value_text)
    case = []
    case.append((1, "case {t}.{v}".format(t=enum_type, v=enum_value_text)))
    case.append((2, "break;"))
    case.append((2, ""))
    return case


def after_last_x(text, x):
    """
    after_last_x(str, str) -> str

    >>> after_last_x("enum class Actions", " ")
    'Actions'
    >>> after_last_x("enum Actions", " ")
    'Actions'
    """
    i = text.rfind(x)
    if i > -1:
        return text[i+1:]
    return None


def before_first_x(text, x):
    """
    before_first_x(str, str) -> str

    >>> before_first_x("enum class Actions", " ")
    'enum'
    >>> before_first_x("enum Actions : byte", " : ")
    'enum Actions'
    >>> before_first_x("enum Actions : ", " : ")
    'enum Actions'
    """
    i = text.find(x)
    if i > -1:
        return text[:i]
    return None


def extract_enum_type(text):
    """
    extract_enum_type(str) -> str

    >>> extract_enum_type("enum class Actions")
    'Actions'
    >>> extract_enum_type("enum Actions : byte")
    'Actions'
    """
    stripped_parent = before_first_x(text, " : ") or text
    return after_last_x(stripped_parent, " ")


def convert_enum_to_switch(enum_value_textblock):
    """
    convert_enum_to_switch(str, object) -> str

    >>> expected = [(1, 'case Actions.Idle:'), (2, 'break;'), (2, ''), (1, 'case Actions.Grab:'), (2, 'break;'), (2, ''), (1, 'case Actions.Place:'), (2, 'break;'), (2, ''), (1, 'case Actions.Throw:'), (2, 'break;'), (2, '')]
    >>> def test(case):
    ...     for a,b in zip(convert_enum_to_switch(case), expected):
    ...         assert a == b, "Output {0} didn't match expected {1}".format(a,b)
    >>>
    >>> enum_text = '''
    ... public enum Actions
    ... {
    ...     Idle,
    ...     Grab,
    ...     Place,
    ...     Throw,
    ... }
    ... '''
    >>> test(enum_text)

    >>> enum_text_explicit = '''enum Actions : int
    ... {
    ...     Idle = 0,
    ...     Grab = 1,
    ...     Place = 2,
    ...     Throw = 3,
    ... }
    ... '''
    >>> test(enum_text_explicit)

    >>> enum_text_cpp = '''enum class Actions
    ... {
    ...     Idle,
    ...     Grab,
    ...     Place,
    ...     Throw
    ... };
    ... '''
    >>> test(enum_text_cpp)

    """
    enum_value_lines = enum_value_textblock.split('\n')
    enum_value_lines = [line.strip() for line in enum_value_lines if re.search("[{}]", line) is None]
    enum_value_lines = [line for line in enum_value_lines if len(line) > 0]
    enum_type = extract_enum_type(enum_value_lines[0])
    if enum_type:
        enum_value_lines = enum_value_lines[1:] # skip typename
    else:
        enum_type = "EnumType"
    enum_value_lines = [line.strip() for line in enum_value_lines if re.search(line, "[{}]") is None]
    case_pairs = [__convert_enum_to_case(enum_type, case) for case in enum_value_lines]
    case_lines = []
    for a in case_pairs:
        case_lines.extend(a)
    return case_lines




def _test():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    _test()
