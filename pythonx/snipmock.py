#! /usr/bin/env python

class SnippetUtil():
    indent = 0
    def mkline(self, text):
        if len(text) == 0:
            return ""
        else:
            return (" " * self.indent) + text
    def shift(self, i=4):
        self.indent += i
    def unshift(self, i=4):
        self.indent -= i

class VimModule():
    def eval(self, str):
        return "4"
