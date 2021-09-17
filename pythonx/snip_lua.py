#! /usr/bin/env python

import re


def _search_and_return_groups_from_regex(buffer, regex):
    for line in buffer:
        match = regex.match(line)
        if match:
            g = list(match.groups())
            g.append(None)
            g.append(None)
            return g[0], g[1]
    return None, None


def get_lua_classname(basename, buffer, cursor):
    cur_line = cursor[0]
    lines = buffer[:cur_line]
    lines.reverse()
    tablename, invoker = _search_and_return_groups_from_regex(
        lines, re.compile(r"^function (\w+)([:\.])(\w+)")
    )

    class_re = re.compile(r"local (\w*) = [cC]lass")
    if not tablename:
        # class.lua
        tablename, _ = _search_and_return_groups_from_regex(lines, class_re)
        invoker = ":"
    if not tablename:
        # class.lua
        tablename, _ = _search_and_return_groups_from_regex(buffer, class_re)
        invoker = ":"
    if not tablename:
        # Table-scoped functions.
        tablename, _ = _search_and_return_groups_from_regex(
            buffer, re.compile(r"local (" + basename + ") = ", re.IGNORECASE)
        )
        invoker = "."
    if not tablename:
        # No scope for functions -- dump in global namespace.
        tablename = ""
        invoker = ""
    return tablename, invoker


# pytest
#
def _testwrap(bufstr):
    buf = bufstr.split("\n")
    return buf, [0, len(buf)]


def test_get_lua_classname():
    buf, endcursor = _testwrap(
        """
local PopupDialog = require("screens/dialogs/popupdialog")

local EquipDialog = Class(PopupDialog, function(self, controller)
    self._base._ctor(self, "EquipDialog", controller)
    self:Init()
end)

local EquipDialogIcon = Class(Image, function()
    self._base._ctor(self, "EquipDialogIcon")
    self.root = Image()
end)

function EquipDialog:Init()
    self.root = Widget()
end

"""
    )
    r = get_lua_classname("equipdialog", buf, endcursor)
    assert r[0] == "EquipDialog"
    assert r[1] == ":"

    after_equip_class = 7
    after_icon_class = 12
    after_equip_func = 16
    r = get_lua_classname("equipdialog", buf, [0, after_equip_class])
    assert buf[after_equip_class] == ""
    assert r[0] == "EquipDialog"
    assert r[1] == ":"
    r = get_lua_classname("equipdialog", buf, [0, after_icon_class])
    assert buf[after_icon_class] == ""
    assert r[0] == "EquipDialogIcon"
    assert r[1] == ":"
    r = get_lua_classname("equipdialog", buf, [0, after_equip_func])
    assert buf[after_equip_func] == ""
    assert r[0] == "EquipDialog"
    assert r[1] == ":"

    buf, endcursor = _testwrap(
        """
local not_template = {}

function hi()
    return "hello"
end
"""
    )
    r = get_lua_classname("template", buf, endcursor)
    assert r[0] == ""
    assert r[1] == ""

    buf, endcursor = _testwrap(
        """
local template = {}

local function hi()
    return "hello"
end
"""
    )
    r = get_lua_classname("template", buf, endcursor)
    assert r[0] == "template"
    assert r[1] == "."
