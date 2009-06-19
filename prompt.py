#!/usr/bin/env python

'''prompt

Take a format string, parse any template variables inside, and output
the result.  Useful for putting information about the current repository into
a bash prompt.
'''

import re


def prompt(ui, repo, fs):
    """Take a format string, parse any variables, and output the result."""
    
    def _status(m):
        stat = repo.status()[:4]
        return '!' if any(stat[:3]) else '?' if stat[-1] else ''
    
    patterns = {
        r'\{branch\}': lambda m: repo[-1].branch(),
        r'\{status\}': _status,
    }
    
    for pattern, repl in patterns.items():
        fs = re.sub(pattern, repl, fs)
    print fs

cmdtable = {
    # "command-name": (function-call, options-list, help-string)
    "prompt": (prompt, [],
    #                 [('s', 'short', None, 'print short form'),
     #                 ('l', 'long', None, 'print long form')],
                     "hg prompt 'FORMATSTRING'")
}