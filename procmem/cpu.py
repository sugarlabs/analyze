# Copyright (C) 2007, Eduardo Silva <edsiper@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import string
import gobject
import cairo

class CPU_Usage(object):
    _last_jiffies = 0
    _times = 0

    def __init__(self):
        self._CPU_HZ = os.sysconf(2)

    def _get_CPU_data(self):
        # Uptime info
        stat_file = "/proc/stat"

        try:
            infile = file(stat_file, "r")
        except:
            print "Error trying uptime file"
            return -1

        stat_line = infile.readline()
        cpu_info = string.split(stat_line, ' ')
        infile.close()

        return cpu_info
    
    def get_CPU_usage(self, frequency):
        
        cpu_info = self._get_CPU_data()
        
        used_jiffies = (int(cpu_info[2]) + int(cpu_info[3]) + int(cpu_info[4]))

        if self._times ==0:
            self._last_jiffies = used_jiffies
            self._times +=1
            return 0

        new_ujiffies = (used_jiffies - self._last_jiffies)
        new_ajiffies = ((frequency/1000) * self._CPU_HZ)

        if new_ajiffies <= 0:
            pcpu = 0.0
        else:
            pcpu = ((new_ujiffies*100)/new_ajiffies)

        if pcpu >100:
            pcpu = 100

        self._times +=1
        self._last_jiffies = used_jiffies

        return pcpu

