# Copyright (C) 2006-2007, Eduardo Silva <edsiper@gmail.com>
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
import re
import sys
import string

_PROCFS_PATH = "/proc/"
_PROCFS_STAT_FILE = "stat"

class ProcInfo(object):
    def __init__(self):
        self.proc_list = self.Get_PID_List()

    # Returns Process List
    def Get_PID_List(self):
        list = []
        
        # Exists our procfs ?
        if os.path.isdir(_PROCFS_PATH):
            # around dir entries
            for f in os.listdir(_PROCFS_PATH):
                if os.path.isdir(_PROCFS_PATH+f) & str.isdigit(f):
                        list.append(int(f))

        return list
    
    def MemoryInfo(self, pid):
        # Path
        pidfile = _PROCFS_PATH + str(pid) + "/stat"
        try:
            infile = open(pidfile, "r")
        except:
            print "Error trying " + pidfile
            return None

        # Parsing data , check 'man 5 proc' for details
        stat_data = infile.read()
        infile.close()

        process_name = self._get_process_name(stat_data)
        data = self._get_safe_split(stat_data)

        state_dic = {
                    'R': 'Running',
                    'S': 'Sleeping', 
                    'D': 'Disk sleep',
                    'Z': 'Zombie', 
                    'T': 'Traced/Stopped', 
                    'W': 'Paging'
                    }
        
        # user and group owners
        pidstat = os.stat(pidfile)
        info = {
            'pid': int(data[0]), # Process ID
            'name': process_name,
            'state': data[2], # Process State, ex: R|S|D|Z|T|W
            'state_name': state_dic[data[2]], # Process State name, ex: Running, sleeping, Zombie, etc
            'ppid': int(data[3]), # Parent process ID
            'utime': int(data[13]), # Used jiffies in user mode
            'stime': int(data[14]), # Used jiffies in kernel mode
            'start_time': int(data[21]), # Process time from system boot (jiffies)
            'vsize': int(data[22]), # Virtual memory size used (bytes)
            'rss': int(data[23])*4,    # Resident Set Size (bytes)
            'user_id': pidstat.st_uid, # process owner
            'group_id': pidstat.st_gid # owner group
        }

        return info
    
    # Return the process name
    def _get_process_name(self, data):
        m = re.search("\(.*\)", data)
        return m.string[m.start()+1:m.end()-1]

    def _get_safe_split(self, data):
        new_data = re.sub("\(.*\)", '()', data)
        return new_data.split()

    # Returns the CPU usage expressed in Jiffies
    def get_CPU_usage(self, cpu_hz, used_jiffies, start_time):
        # Uptime info
        uptime_file = _PROCFS_PATH + "/uptime"
        try:
            infile = file(uptime_file, "r")
        except:
            print "Error opening uptime file"
            return None
        
        uptime_line = infile.readline()
        uptime = string.split(uptime_line, " ",2)
        
        infile.close()
                
        # System uptime, from /proc/uptime
        uptime = float(uptime[0])

        # Jiffies
        avail_jiffies = (uptime * cpu_hz) - start_time
        cpu_usage = {'used_jiffies': used_jiffies, 'avail_jiffies': avail_jiffies}

        return cpu_usage

    def get_CPU_system_stat(self):
        stat_path = "%s%s" % (_PROCFS_PATH, _PROCFS_STAT_FILE)
        try:
            stat = file(stat_path, "r")
            cpu_info = stat.readline().split()
        except:
            print "Error opening %s file" % stat_path
            return None

        return cpu_info
