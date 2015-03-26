tidybattery
===========

Lightweight GTK tray battery monitor. The original project by [decayofmind](https://github.com/decayofmind/tidybattery) is a fork of slimebattery rewritten in Python.  This project is a fork of that with additions of more levels of icon notification and enabling of clicking on the icon to launch a custom command (like the command for the system power manager).

## Setup

Simplest method is to just git clone and be sure you have Python2.  Then run `./tidybattery.py`.  To enable left-click on the icon specify the `-c` or `--command` option when you run the command.  Example:
```
./tidybattery.py -c xfce4-power-manager-settings
```
It might also be of use to move the `.py` file to `/usr/bin` or symlink it there so that you can call the program without the path.  Add the command to your startups to have the icon available after boot.
