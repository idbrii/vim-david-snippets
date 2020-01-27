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


def _test():
    import doctest
    doctest.testmod()
if __name__ == '__main__':
    _test()
