'''Test output of {branch}.'''

from nose import *
from util import *
from mercurial import commands


@with_setup(setup_sandbox, teardown_sandbox)
def test_default_branch():
    output = prompt(fs='{branch}')
    assert output == 'default'
    
    output = prompt(fs='{on {branch}}')
    assert output == 'on default'


@with_setup(setup_sandbox, teardown_sandbox)
def test_non_default_branch():
    commands.branch(get_sandbox_ui(), get_sandbox_repo(), 'test')
    
    output = prompt(fs='{branch}')
    assert output == 'test'
    
    output = prompt(fs='{on the {branch} branch}')
    assert output == 'on the test branch'


@with_setup(setup_sandbox, teardown_sandbox)
def test_quiet_filter():
    output = prompt(fs='{branch|quiet}')
    assert output == ''
    
    output = prompt(fs='{on {branch|quiet}}')
    assert output == ''
    
    commands.branch(get_sandbox_ui(), get_sandbox_repo(), 'test')
    
    output = prompt(fs='{branch|quiet}')
    assert output == 'test'
    
    output = prompt(fs='{on the {branch|quiet} branch}')
    assert output == 'on the test branch'
