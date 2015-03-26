#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       

import gtk
import gobject
import subprocess
import os
import argparse

ACPI_CMD = 'acpi'
TIMEOUT = 2

b = {}
b['empty'] = {'icon': 'battery-empty', 'charge_icon': 'battery-empty-charging', 'percent': 10}
b['caution'] = {'icon': 'battery-caution', 'charge_icon': 'battery-caution-charging', 'percent': 20}
b['low'] = {'icon': 'battery-low', 'charge_icon': 'battery-low-charging', 'percent': 40}
b['fair'] = {'icon': 'battery-fair', 'charge_icon': 'battery-fair-charging', 'percent': 60}
b['good'] = {'icon': 'battery-good', 'charge_icon': 'battery-good-charging', 'percent': 80}
b['full'] = {'icon': 'battery-full', 'charge_icon': 'battery-full-charging', 'percent': 100}
b['full_adapter'] = {'icon': 'gnome-power-manager', 'percent': 100}

class MainApp:
        def __init__(self):
                self.last_icon = {}
                parser = argparse.ArgumentParser()
                parser.add_argument("-c", "--command", help='The command to run when left-clicking on the battery status icon.')
                self.args = vars(parser.parse_args())
                self.icon = gtk.StatusIcon()
                self.icon.set_from_stock(gtk.STOCK_HOME)
                self.icon.connect('activate', self.left_click)
                self.update_icon()
                gobject.timeout_add_seconds(TIMEOUT,self.update_icon)

        def left_click(self, icon):
                if 'command' in self.args:
                        os.system(self.args['command'])
                else:
                        notify = 'notify-send -i "battery" -t 10000 "{title}" "{description}"'
                        os.system(notify.format(title='Command not specified', description='To be able to left click on the status icon, you must specify a command to run on left click of the icon using the -c flag.'))

        def get_battery_info(self):
                text = subprocess.check_output(ACPI_CMD).strip('\n')
                if not 'Battery' in text:
                        return {'state':"Unknown",
                                'percentage':0,
                                'tooltip':""
                                }
                data = text.split(',')
                state = data[0].split(':')[1].strip(' ')
                percentage_str = data[1].strip(' %')
                percentage = int(percentage_str)
                time = data[2].split(' ')[1]
                return {'state':state,
                                'percentage':percentage,
                                'tooltip': 'Battery is ' + state + ' (' + percentage_str + '%)\n ' + time + ' remaining',
																'time': time,
                                }

        def get_icon(self, state, percentage):
                icon = b['full']
                icon['state'] = 'icon'
                if state == 'Full':
                        icon = b['full_adapter']
                        icon['state'] = 'icon'
                        return icon
                for key in b:
                        if percentage <= b[key]['percent'] and key != 'full_adapter':
                                icon = b[key]
                                if state == 'Discharging':
                                        icon['state'] = 'icon'
                                else:
                                        icon['state'] = 'charge_icon'
                return icon

        def update_icon(self):
                info = self.get_battery_info()
                icon = self.get_icon(info['state'],info['percentage'])
                self.icon.set_from_icon_name(icon[icon['state']])
                self.icon.set_tooltip_text(info['tooltip'])
                return True

if __name__ == "__main__":
        try:
                MainApp()
                gtk.main()
        except KeyboardInterrupt:
                pass
