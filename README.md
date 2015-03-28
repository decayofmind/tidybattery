tidybattery
===========

Lightweight GTK tray battery monitor. The original project by [decayofmind](https://github.com/decayofmind/tidybattery) is a fork of [slimebattery](https://github.com/Enrix835/slimebattery) rewritten in Python.  This project is a fork of that with additions of more levels of icon notification and enabling of clicking on the icon to launch a custom command (like the command for the system power manager).

## Setup
Put into your path, as an example the following would work
```
cd [path/where/tidybattery/will/live]
git clone https://github.com/nalipaz/tidybattery.git
cd tidybattery
sudo ln -s `pwd`/tidybattery.py /usr/bin/tidybattery1
```
Create a config file at `~/.tidybattery`, just run the following to generate a default config file which you could modify if needed:
```
echo -e "[general]\ncommand = xfce4-power-manager-settings\n\n[empty]\nicon = battery-empty\ncharge_icon = battery-empty-charging\npercent = 0\n\n[caution]\nicon = battery-caution\ncharge_icon = battery-caution-charging\npercent = 10\n\n[low]\nicon = battery-low\ncharge_icon = battery-low-charging\npercent = 20\n\n[fair]\nicon = battery-fair\ncharge_icon = battery-fair-charging\npercent = 45\n\n[good]\nicon = battery-good\ncharge_icon = battery-good-charging\npercent = 70\n\n[full]\nicon = battery-full\ncharge_icon = battery-full-charging\npercent = 95\n\n[full_adapter]\nicon = gnome-power-manager\npercent = 100" > ~/.tidybattery
```
Alternatively, you can copy the config file below and edit as you need:
```
[general]
command = xfce4-power-manager-settings

[empty]
icon = battery-empty
charge_icon = battery-empty-charging
percent = 0

[caution]
icon = battery-caution
charge_icon = battery-caution-charging
percent = 10

[low]
icon = battery-low
charge_icon = battery-low-charging
percent = 20

[fair]
icon = battery-fair
charge_icon = battery-fair-charging
percent = 45

[good]
icon = battery-good
charge_icon = battery-good-charging
percent = 70

[full]
icon = battery-full
charge_icon = battery-full-charging
percent = 95

[full_adapter]
icon = gnome-power-manager
percent = 100
```
