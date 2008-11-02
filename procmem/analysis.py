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

import proc, proc_smaps

class Analysis:
    
    pid = 0
    
    def __init__(self, pid):
        self.pid = pid
    
    def SMaps(self):
        smaps =    proc_smaps.ProcSmaps(self.pid)
        private_dirty = 0
        shared_dirty = 0
        referenced = 0

        for map in smaps.mappings:
            private_dirty += map.private_dirty
            shared_dirty  += map.shared_dirty
            referenced += map.referenced

        smaps = {"private_dirty": int(private_dirty), \
                    "shared_dirty": int(shared_dirty),\
                    "referenced": int(referenced)}

        return smaps
    
    def ApproxRealMemoryUsage(self):
        maps = proc_smaps.ProcMaps(self.pid)
        size = (maps.clean_size/1024)

        return size
    
