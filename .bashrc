# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi


# Help me out if zsh exists and I have no control over my shell for some reason
ZSH_EXECUTABLE=$(grep zsh /etc/shells)
if [ $? -eq 0 ]; then
  if [[ $- == *i* ]]; then
    if ! echo ${BASH_EXECUTION_STRING} | grep -E '^scp.*|^rsync.*|^git.*' >> /dev/null; then
      # switch to zsh
      export LANG=en_US.UTF-8
      exec ${ZSH_EXECUTABLE} -i
    fi
  fi
fi


