#!/bin/bash
#geometry="1920x1080"
#eometry="1280x1024"
geometry="1600x1200"
depth="24"
xstartup="$HOME/.vnc/xstartup"

# Create the xstartup file if it doesn't exist
if [ ! -f $xstartup ]; then
  mkdir -p $(dirname $xstartup)
  echo -e "#!/bin/bash\nxrdb $HOME/.Xresources\nstartxfce4 &" > $xstartup
  chmod +x $xstartup
fi

# Start the VNC server
for desktop in $(seq 1 11); do
  vncserver :$desktop -geometry $geometry -depth $depth -localhost no
done
