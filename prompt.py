#!/usr/bin/env python

'''prompt

Take a format string, parse any template variables inside, and output
the result.  Useful for putting information about the current repository into
a bash prompt.
'''

import re
from mercurial import extensions

def with_groups(m, out):
    g = m.groups()
    if any(g) and not all(g):
        print 'ERROR'
    return ("%s" + out + "%s") % (g[0][:-1] if g[0] else '',
                                  g[1][1:]  if g[1] else '')
    
    

def prompt(ui, repo, fs):
    """Take a format string, parse any variables, and output the result."""
    
    def _branch(m):
        return with_groups(m, repo[-1].branch())
    
    def _status(m):
        st = repo.status(unknown=True)[:5]
        return with_groups(m, '!' if any(st[:4]) else '?' if st[-1] else '')
    
    def _bookmark(m):
        try:
            return extensions.find('bookmarks').current(repo)
        except KeyError:
            return ''
    
    tag_start = r'\{([^{}]*?\{)?'
    tag_end = r'(\}[^{}]*?)?\}'
    patterns = {
        'branch': _branch,
        'status': _status,
        'bookmark': _bookmark,
    }
    
    for tag, repl in patterns.items():
        fs = re.sub(tag_start + tag + tag_end, repl, fs)
    print fs

cmdtable = {
    # "command-name": (function-call, options-list, help-string)
    "prompt": (prompt, [],
    #                 [('s', 'short', None, 'print short form'),
     #                 ('l', 'long', None, 'print long form')],
                     "hg prompt 'FORMATSTRING'")
}