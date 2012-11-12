# Path to your oh-my-zsh configuration.
export ZSH=$HOME/.oh-my-zsh

if [ -z ${DISPLAY} ]; then
  ZSH_THEME="imajes"
else
  ZSH_THEME="brandoma"
fi 

# Set to this to use case-sensitive completion
CASE_SENSITIVE="true"

# Comment this out to disable weekly auto-update checks
DISABLE_AUTO_UPDATE="true"

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
COMPLETION_WAITING_DOTS="false"

plugins=(git vi-mode django pip)

source $ZSH/oh-my-zsh.sh

bindkey -M viins '^r' history-incremental-search-backward
bindkey -M vicmd '^r' history-incremental-search-backward

export LANG=en_US.UTF-8

source /etc/profile

# Prefer VIM if installed
if [ -x $(which vim) ]; then
  export EDITOR=vim
fi

# plz dont ask..
if [ -d "/opt/python2.7/bin" ]; then
  export PATH="/opt/python2.7/bin:${PATH}"
fi

# NetBSD
if [ $(uname -s) = "NetBSD" ]; then
  if [ -x "/usr/pkg/gnu/bin/ls" ]; then
    alias ls="/usr/pkg/gnu/bin/ls --color=always"
  fi
fi

umask 022
