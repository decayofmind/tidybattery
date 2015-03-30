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
import ConfigParser

ACPI_CMD = 'acpi'
TIMEOUT = 2
config = False
config_path = os.path.expanduser('~/.tidybattery')

try:
    with open(config_path) as f:
        config = ConfigParser.SafeConfigParser({'command': None, 'icon': 'battery-full', 'charge_icon': 'battery-full-charging', 'percent': 100})
        config.read(config_path)
        b = {}
        for key in config._sections:
            if key in ('empty', 'caution', 'low', 'fair', 'good', 'full'):
                b[key] = config._sections[key]
                b[key]['percent'] = int(b[key]['percent'])
except IOError:
    print 'There must be a config file (~/.tidybattery) setup.  See the README.md for documentation.'
    exit

if config:
    class MainApp:
        def __init__(self):
            self.last_icon = {}
            self.icon = gtk.StatusIcon()
            self.icon.set_from_stock(gtk.STOCK_HOME)
            self.icon.connect('activate', self.left_click)
            self.update_icon()
            gobject.timeout_add_seconds(TIMEOUT,self.update_icon)

        def left_click(self, icon):
            if config._sections['general']['command'] != None:
                os.system(config._sections['general']['command'])
            else:
                notify = 'notify-send -i "battery" -t 10000 "{title}" "{description}"'
                os.system(notify.format(title='Command not specified', description='To be able to left click on the status icon, you must specify a command to run on left click of the icon using the \`-c\` flag or the \`--command\` option.  Try \`--help\` for more information.'))

        def get_battery_info(self):
            text = subprocess.check_output(ACPI_CMD).strip('\n')
            if not 'Battery' in text:
                return {
                    'state': "Unknown",
                    'percentage': 0,
                    'tooltip': ""
                }
            data = text.split(',')
            state = data[0].split(':')[1].strip(' ')
            percentage_str = data[1].strip(' %')
            percentage = int(percentage_str)
            time = '' if state in ('Full', 'Unknown') else data[2].split(' ')[1]
            tooltip = 'Battery is {state}' if state in ('Full', 'Unknown') else 'Battery is {state} ({percentage}%)\n {time} remaining'
            return {
                'state': state,
                'percentage': percentage,
                'tooltip': tooltip.format(state=state, percentage=percentage, time=time),
                'time': time,
            }

        def get_icon(self, state, percentage):
            icon = b['full']
            icon['state'] = 'icon'
            if state == 'Full':
                icon = config._sections['full_adapter']
                icon['state'] = 'icon'
                return icon
            closest_match = 0
            for key in b:
                if percentage >= b[key]['percent'] and b[key]['percent'] > closest_match:
                    closest_match = b[key]['percent']
                    icon = b[key]
                    icon['state'] = 'icon' if state == 'Discharging' else 'charge_icon'
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

