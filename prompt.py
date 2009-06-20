#!/usr/bin/env python

'''get repository information for use in a shell prompt

Take a string, parse any special variables inside, and output the result.

Useful mostly for putting information about the current repository into
a shell prompt.
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
    '''get repository information for use in a shell prompt
    
    Take a string and output it for use in a shell prompt. You can use 
    keywords in curly braces:
    
        $ hg prompt "currently on {branch}"
        currently on default
    
    You can also use an extended form of any keyword:
    
        {optional text here{keyword}more optional text}
    
    This will expand the inner {keyword} and output it along with the extra
    text only if the {keyword} expands successfully.  This is useful if a
    keyword that may not always apply to the current state and you have some
    text that you would like to see only if it is appropriate:
    
        $ hg prompt "currently at {bookmark}"
        currently at 
        $ hg prompt "{currently at {bookmark}}"
        $ hg bookmark my-bookmark
        $ hg prompt "{currently at {bookmark}}"
        currently at my-bookmark
    
    The following keywords are available:
    
    - bookmark: the current bookmark
    - branch: the current branch
    - status: "!" if the current repository contains files that have been
        modified, added, removed, or deleted, otherwise "?" if it contains
        untracked (and not ignored) files, otherwise nothing.
    '''
    
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
    "prompt": (prompt, [], 'hg prompt STRING')
}