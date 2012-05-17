xsetroot -cursor_name left_ptr
xrdb -merge ~/.Xresources
xset b off
if [ -x "/usr/local/bin/vmtoolsd" ]; then
  /usr/local/bin/vmtoolsd -n vmusr &
fi
exec scrotwm
