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
        branch = repo[-1].branch()
        return with_groups(m, branch) if branch else ''
    
    def _status(m):
        st = repo.status(unknown=True)[:5]
        flag = '!' if any(st[:4]) else '?' if st[-1] else ''
        return with_groups(m, flag) if flag else ''
    
    def _bookmark(m):
        try:
            book = extensions.find('bookmarks').current(repo)
            return with_groups(m, book) if book else ''
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
    ui.status(fs)

cmdtable = {
    "prompt": (prompt, [], 'hg prompt "FORMATSTRING"')
}