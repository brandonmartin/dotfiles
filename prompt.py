#!/usr/bin/env python

'''prompt

Take a format string, parse any template variables inside, and output
the result.  Useful for putting information about the current repository into
a bash prompt.
'''

from mercurial import hg

def prompt(ui, repo, fs):
    """Take a format string, parse any variables, and output the result."""
    ui.write(fs)

cmdtable = {
    # "command-name": (function-call, options-list, help-string)
    "prompt": (prompt, [],
    #                 [('s', 'short', None, 'print short form'),
     #                 ('l', 'long', None, 'print long form')],
                     "hg prompt 'FORMATSTRING'")
}