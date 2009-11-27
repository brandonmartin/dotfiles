"""Utilities for writing unit tests for hg-prompt."""

import os, shutil, sys
from mercurial import cmdutil, commands, hg, ui

pkg_path = os.path.realpath(__file__)
sys.path =[os.path.split(os.path.split(pkg_path)[0])[0]] + sys.path
from prompt import prompt as _prompt

_ui = ui.ui()
def prompt(fs=''):
    _ui.pushbuffer()
    _prompt(_ui, get_sandbox_repo(), fs=fs)
    output = _ui.popbuffer()
    
    print output
    return output

sandbox_path = os.path.join(os.path.realpath('.'), 'sandbox')

def setup_sandbox():
    os.mkdir(sandbox_path)
    os.chdir(sandbox_path)
    
    commands.init(_ui)

def teardown_sandbox():
    os.chdir(os.path.realpath(os.path.join(sandbox_path, os.pardir)))
    shutil.rmtree(sandbox_path)

def get_sandbox_repo():
    return hg.repository(_ui, sandbox_path)

def get_sandbox_ui():
    return _ui