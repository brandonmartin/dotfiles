#!/usr/bin/env python

'''get repository information for use in a shell prompt

Take a string, parse any special variables inside, and output the result.

Useful mostly for putting information about the current repository into
a shell prompt.
'''

import re
import os
import subprocess
from os import path
from mercurial import extensions, hg, cmdutil

CACHE_PATH = ".hg/prompt/cache"

def _with_groups(g, out):
    if any(g) and not all(g):
        print 'ERROR'
    return ("%s" + out + "%s") % (g[0][:-1] if g[0] else '',
                                  g[1][1:]  if g[1] else '')    

def prompt(ui, repo, fs='', **opts):
    '''get repository information for use in a shell prompt
    
    Take a string and output it for use in a shell prompt. You can use 
    keywords in curly braces:
    
        $ hg prompt "currently on {branch}"
        currently on default
    
    You can also use an extended form of any keyword:
    
        {optional text here{keyword}more optional text}
    
    This will expand the inner {keyword} and output it along with the extra
    text only if the {keyword} expands successfully.  This is useful if you
    have a keyword that may not always apply to the current state and you 
    have some text that you would like to see only if it is appropriate:
    
        $ hg prompt "currently at {bookmark}"
        currently at 
        $ hg prompt "{currently at {bookmark}}"
        $ hg bookmark my-bookmark
        $ hg prompt "{currently at {bookmark}}"
        currently at my-bookmark
    
    The following keywords are available:
    
    - bookmark: the current bookmark
    - branch: the current branch
    - incoming: this keyword prints nothing on its own.  If the default
        path contains incoming changesets the extra text will be expanded.
        For example:
            '{incoming changes{incoming}}' will expand to
            'incoming changes' if there are changes, '' otherwise.
    - incoming|count: the number of incoming changesets if greater than 0
    - outgoing: this keyword prints nothing on its own.  If the current
        repository contains outgoing changesets (to default) the extra text
        will be expanded. For example:
            '{outgoing changes{outgoing}}' will expand to
            'outgoing changes' if there are changes, '' otherwise.
    - outgoing|count: the number of outgoing changesets if greater than 0
    - root: the full path to the root of the current repository, without a 
        trailing slash
    - root|basename: the directory name of the root of the current
        repository.  For example, if the repository is in '/home/u/myrepo'
        then this keyword would expand to 'myrepo'.
    - status: "!" if the current repository contains files that have been
        modified, added, removed, or deleted, otherwise "?" if it contains
        untracked (and not ignored) files, otherwise nothing.
    '''
    
    def _branch(m):
        branch = repo.dirstate.branch()
        return _with_groups(m.groups(), branch) if branch else ''
    
    def _status(m):
        st = repo.status(unknown=True)[:5]
        flag = '!' if any(st[:4]) else '?' if st[-1] else ''
        return _with_groups(m.groups(), flag) if flag else ''
    
    def _bookmark(m):
        try:
            book = extensions.find('bookmarks').current(repo)
            return _with_groups(m.groups(), book) if book else ''
        except KeyError:
            return ''
    
    def _root(m):
        return _with_groups(m.groups(), repo.root) if repo.root else ''
    
    def _basename(m):
        return _with_groups(m.groups(), path.basename(repo.root)) if repo.root else ''
    
    def _incoming(m):
        g = m.groups()
        out_g = (g[0],) + (g[-1],)
        
        cache = path.join(repo.root, CACHE_PATH, 'incoming')
        cache_out = cache + '.out'
        
        subprocess.Popen(['hg', 'prompt', '--cache-incoming'])
        
        if path.isfile(cache):
            with open(cache) as c:
                count = len(c.readlines())
                if g[1]:
                    return _with_groups(out_g, str(count)) if count else ''
                else:
                    return _with_groups(out_g, '') if count else ''
        else:
            return ''
    
    def _outgoing(m):
        g = m.groups()
        out_g = (g[0],) + (g[-1],)
        
        cache = path.join(repo.root, CACHE_PATH, 'outgoing')
        if path.isfile(cache):
            with open(cache) as c:
                count = c.readline().strip()
                if g[1]:
                    return _with_groups(out_g, count) if int(count) else ''
                else:
                    return _with_groups(out_g, '') if int(count) else ''
        else:
            return ''
    
    tag_start = r'\{([^{}]*?\{)?'
    tag_end = r'(\}[^{}]*?)?\}'
    patterns = {
        'branch': _branch,
        'status': _status,
        'bookmark': _bookmark,
        'root': _root,
        'root\|basename': _basename,
        'incoming(\|count)?': _incoming,
        'outgoing(\|count)?': _outgoing,
    }
    
    if opts.get("cache_incoming"):
        cache = path.join(repo.root, CACHE_PATH, 'incoming')
        c_tmp = cache + '.temp'
        subprocess.call(['hg', 'incoming', '--quiet'], stdout=file(c_tmp, 'w'))
        os.rename(c_tmp, cache)
        return
    
    for tag, repl in patterns.items():
        fs = re.sub(tag_start + tag + tag_end, repl, fs)
    ui.status(fs)

cmdtable = {
    "prompt": 
    (prompt, [
        ('', 'cache-incoming', None, 'used internally by hg-prompt'),
        ('', 'cache-outgoing', None, 'used internally by hg-prompt'),
    ],
    'hg prompt STRING')
}