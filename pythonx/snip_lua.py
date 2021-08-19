#! /usr/bin/env python

import re

def _search_and_return_first_group_from_regex(buffer, regex):
	for line in buffer:
		match = regex.match(line)
		if match:
			return match.group(1)
	return None


def get_lua_classname(basename, buffer):
	# class.lua
	tablename = _search_and_return_first_group_from_regex(buffer, re.compile("local (\w*) = [cC]lass"))
	invoker = ':'
	if not tablename:
		# Table-scoped functions.
		tablename = _search_and_return_first_group_from_regex(buffer, re.compile("local ("+ basename +") = ", re.IGNORECASE))
		invoker = '.'
	if not tablename:
		# No scope for functions -- dump in global namespace.
		tablename = ''
		invoker = ''
	return tablename, invoker


