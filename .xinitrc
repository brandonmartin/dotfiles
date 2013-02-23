xsetroot -cursor_name left_ptr
xrdb -merge ~/.Xresources
xset b off
if [ -x "/usr/local/bin/vmtoolsd" ]; then
  /usr/local/bin/vmtoolsd -n vmusr &
fi

if [ -x "/usr/bin/VBoxClient-all" ]; then
  /usr/bin/VBoxClient-all
fi

exec spectrwm
