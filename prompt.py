#!/usr/bin/env python

from __future__ import with_statement

'''get repository information for use in a shell prompt

Take a string, parse any special variables inside, and output the result.

Useful mostly for putting information about the current repository into
a shell prompt.
'''

import re
import os
import subprocess
from datetime import datetime, timedelta
from os import path
from mercurial import extensions

CACHE_PATH = ".hg/prompt/cache"
CACHE_TIMEOUT = timedelta(minutes=15)

def _cache_remote(repo, kind):
    cache = path.join(repo.root, CACHE_PATH, kind)
    c_tmp = cache + '.temp'
    
    # This is kind of a hack and I feel a little bit dirty for doing it.
    IGNORE = open('NUL:','w') if subprocess.mswindows else open('/dev/null','w')
    
    subprocess.call(['hg', kind, '--quiet'], stdout=file(c_tmp, 'w'), stderr=IGNORE)
    os.rename(c_tmp, cache)
    return

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
    
    - bookmark: the current bookmark (requires the bookmarks extension)
    - branch: the current branch
    - rev: the repository-local changeset number of the current parent.  This
        does not take into account merges (which have two parents) -- see the
        'rev|merge' keyword for that.
    - rev|merge: the repository-local changeset number of the changeset
        you're merging with if you're currently merging, otherwise nothing
    - root: the full path to the root of the current repository, without a 
        trailing slash
    - root|basename: the directory name of the root of the current
        repository.  For example, if the repository is in '/home/u/myrepo'
        then this keyword would expand to 'myrepo'.
    - status: "!" if the current repository contains files that have been
        modified, added, removed, or deleted, otherwise "?" if it contains
        untracked (and not ignored) files, otherwise nothing.
    - task: the current task (requires the tasks extension)
    - update: "^" if the current parent is not the tip of the current branch,
        otherwise nothing.  In effect, this lets you see if running 
        'hg update' would do something.
    
    There are also several keywords that deal with the status of remote
    repositories.  They cache their results in .hg/prompt/cache/ and refresh
    approximately every fifteen minutes to avoid overloading remote servers.
    
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
    
    def _task(m):
        try:
            task = extensions.find('tasks').current(repo)
            return _with_groups(m.groups(), task) if task else ''
        except KeyError:
            return ''
    
    def _root(m):
        return _with_groups(m.groups(), repo.root) if repo.root else ''
    
    def _basename(m):
        return _with_groups(m.groups(), path.basename(repo.root)) if repo.root else ''
    
    def _update(m):
        curr = repo[None].parents()[0]
        to = repo[repo.branchtags()[curr.branch()]]
        return _with_groups(m.groups(), '^') if curr != to else ''
    
    def _rev(m):
        g = m.groups()
        out_g = (g[0],) + (g[-1],)
        
        parents = repo[None].parents()
        p = 0 if '|merge' not in g else 1
        p = p if len(parents) > p else None
        
        rev = parents[p].rev() if p is not None else None
        return _with_groups(out_g, str(rev)) if rev else ''
    
    def _remote(kind):
        def _r(m):
            g = m.groups()
            out_g = (g[0],) + (g[-1],)
            
            cache_dir = path.join(repo.root, CACHE_PATH)
            cache = path.join(cache_dir, kind)
            if not path.isdir(cache_dir):
                os.makedirs(cache_dir)
            
            cache_exists = path.isfile(cache)
            
            cache_time = (datetime.fromtimestamp(os.stat(cache).st_mtime)
                          if cache_exists else None)
            if not cache_exists or cache_time < datetime.now() - CACHE_TIMEOUT:
                if not cache_exists:
                    open(cache, 'w').close()
                subprocess.Popen(['hg', 'prompt', '--cache-%s' % kind])
            
            if cache_exists:
                with open(cache) as c:
                    count = len(c.readlines())
                    if g[1]:
                        return _with_groups(out_g, str(count)) if count else ''
                    else:
                        return _with_groups(out_g, '') if count else ''
            else:
                return ''
        return _r
    
    tag_start = r'\{([^{}]*?\{)?'
    tag_end = r'(\}[^{}]*?)?\}'
    patterns = {
        'bookmark': _bookmark,
        'branch': _branch,
        'rev(\|merge)?': _rev,
        'root': _root,
        'root\|basename': _basename,
        'status': _status,
        'task': _task,
        'update': _update,
        
        'incoming(\|count)?': _remote('incoming'),
        'outgoing(\|count)?': _remote('outgoing'),
    }
    
    if opts.get("cache_incoming"):
        _cache_remote(repo, 'incoming')
    
    if opts.get("cache_outgoing"):
        _cache_remote(repo, 'outgoing')
    
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
