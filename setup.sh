#!/usr/bin/env sh
# sets up dotfiles 

BASE="GIT/dotfiles"
LINKS=".bashrc .conkyrc .gitconfig .hgrc .oh-my-zsh"
LINKS="${LINKS} spectrwm.conf .scrotwm.conf .vim .vimrc .xinitrc"
LINKS="${LINKS} .Xresources .zshrc"

if [ -z "${HOME}" ]; then
  echo "Error: \$HOME must be set"
  exit 1
fi


for link in ${LINKS}; do
  if [ -L "${HOME}/${link}" ]; then
    if [ "$(readlink ${HOME}/${link})" = "${BASE}/${link}" ]; then
      continue
    fi
  fi

  if [ -r "${HOME}/${link}" ]; then
    echo mv "${HOME}/${link}" "${HOME}/${link}.dfsetup_bak"
    mv "${HOME}/${link}" "${HOME}/${link}.dfsetup_bak"
  fi

  echo ln -sf "${BASE}/${link}" "${HOME}/${link}"
  ln -sf "${BASE}/${link}" "${HOME}/${link}"

done

echo "you're all set!"
exit 0

