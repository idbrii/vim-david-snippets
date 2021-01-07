#! /usr/bin/env python3

import re

# inflection seems neat for snake -> camel case conversions, but doesn't remove
# leading/trailing underscores.
# import inflection


def _capitalize_group(m):
    g = m.group(2)
    if g:
        return g.capitalize()
    return ''

def basename_to_mixed_case(basename):
    """Convert a snip.basename to a classname in MixedCase.

    basename_to_mixed_case(str) -> str
    >>> basename_to_mixed_case("gameboard_view")
    'GameboardView'
    >>> tests = [
    ...     'get__this_value',
    ...     '_get__this_value',
    ...     '_get__this_value_',
    ...     'get_this_value',
    ...     'get__this__value',
    ... ]
    >>> [basename_to_mixed_case(t) for t in tests]
    ['GetThisValue', 'GetThisValue', 'GetThisValue', 'GetThisValue', 'GetThisValue']
    """
    return re.sub("(_+|^)(.)?", _capitalize_group, basename)


def guess_type_from_decl(typename, varname):
    """Guess the name of the type from the inputs.

    typename and varname are match 1 and 3 from regex:
    /^\s*(\w[^=]+)(\*?) (\S+) = new/

    guess_type_from_decl(str, str) -> str
    """
    if typename == 'var':
        t = varname
        # m_blah/_blah -> blah
        t = re.sub(r"^[mk]?_", '', t)
        if len(t) > 1:
            t = t[0].upper() + t[1:]
        # Guess the variable name is close to the typename.
        # i.e, var list = new List<>
        list_names = [ 'List', 'Items', 'Elements', ]
        dict_names = [ 'Dict', 'Map', ]
        if t in list_names:
            t = "List<>"
        elif t in dict_names:
            t = "Dictionary<>"
        return t
    else:
        # Limited C++ support.
        t = typename
        t = re.sub(r"[*].*$", '', t)
        t = re.sub(r"^const ", '', t)
        t = re.sub(r"^(public|internal|protected|private) ", '', t)
        return t

def _test():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    _test()
