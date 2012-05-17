function collapse_pwd {
    echo $(pwd | sed -e "s,^$HOME,~,")
}

function prompt_char {
    git branch >/dev/null 2>/dev/null && echo '±' && return
    hg root >/dev/null 2>/dev/null && echo '☿' && return
    echo '○'
}

function gen_right_prompt {
    if [ $? = 0 ]; then
        echo "%{$fg_bold[cyan]%}\xe2\x98\xaf%{$reset_color%}" && return
    else
        echo "%{$fg_bold[yellow]%}\xe2\x98\xa2%{$reset_color%}" && return
#        echo '\xe2\x98\xa0' && return
    fi
}

function virtualenv_info {
    [ $VIRTUAL_ENV ] && echo '('`basename $VIRTUAL_ENV`') '
}

function hg_prompt_info {
    hg prompt 2>/dev/null >/dev/null
    if [ $? -eq '0' ]; then
      hg prompt --angle-brackets "\
< on %{$fg_bold[green]%}<branch>%{$reset_color%}>\
< at %{$fg_bold[yellow]%}<tags|%{$reset_color%}, %{$fg[yellow]%}>%{$reset_color%}>\
%{$fg_bold[red]%}<status|modified|unknown><update>%{$reset_color%}<
patches: <patches|join( → )|pre_applied(%{$fg[yellow]%})|post_applied(%{$reset_color%})|pre_unapplied(%{$fg_bold[black]%})|post_unapplied(%{$reset_color%})>>" 2>/dev/null
    fi
}

PROMPT_FULL='%{$fg_bold[magenta]%}%n%{$reset_color%}@%{$fg_bold[magenta]%}%m%{$reset_color%} in %{$fg_bold[cyan]%}$(collapse_pwd)%{$reset_color%}$(hg_prompt_info)$(git_prompt_info)
$(virtualenv_info)$(prompt_char) '

RPROMPT_FULL='$(gen_right_prompt)'

PROMPT_LESS='%{$fg_bold[magenta]%}%n%{$reset_color%}@%{$fg_bold[magenta]%}%m%{$reset_color%} in %{$fg_bold[cyan]%}$(collapse_pwd)%{$reset_color%}
$(prompt_char) '
RPROMPT_LESS='$(gen_right_prompt)'

PROMPT_NONE="$(echo $HOSTNAME | cut -d. -f1)\$ "
RPROMPT_NONE=''

PROMPT="$PROMPT_FULL"
RPROMPT="$RPROMPT_FULL"

ZSH_THEME_GIT_PROMPT_PREFIX=" on %{$fg_bold[green]%}"
ZSH_THEME_GIT_PROMPT_SUFFIX="%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg_bold[red]%}!"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$fg_bold[red]%}?"
ZSH_THEME_GIT_PROMPT_CLEAN=""

function prompt_more {
  PROMPT="$PROMPT_FULL"
  RPROMPT="$RPROMPT_FULL"
}

function prompt_less {
  PROMPT="$PROMPT_LESS"
  RPROMPT="$RPROMPT_LESS"
}

function prompt_none {
  PROMPT="$PROMPT_NONE"
  RPROMPT="$RPROMPT_NONE"
}

