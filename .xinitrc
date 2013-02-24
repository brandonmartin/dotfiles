xsetroot -cursor_name left_ptr
xrdb -merge ~/.Xresources
xset b off
if [ -x "/usr/local/bin/vmtoolsd" ]; then
  /usr/local/bin/vmtoolsd -n vmusr &
fi

if [ -x "/usr/bin/VBoxClient" ]; then
  /usr/bin/VBoxClient --clipboard 
  /usr/bin/VBoxClient --display
  /usr/bin/VBoxClient --checkhostversion
  /usr/bin/VBoxClient --seamless
fi

exec spectrwm
