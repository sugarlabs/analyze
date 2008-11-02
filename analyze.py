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
import logging
from gettext import gettext as _

import gtk
import dbus
import pygtk
import gobject
import pango

from sugar.activity import activity
from sugar import env
from sugar.graphics.toolbutton import ToolButton

# Interfaces
from ps_watcher import PresenceServiceNameWatcher
from network import NetworkView
from xserver import XorgView

class AnalyzeHandler(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        logging.debug('Starting the Analyze activity')
        self.set_title(_('Analyze Activity'))

        self._network = NetworkView()
        self._xserver = XorgView()
        self._ps = PresenceServiceNameWatcher(dbus.SessionBus())

        self._box = gtk.HBox()
        self._box.pack_start(self._network)
        self._box.show()

        self.set_canvas(self._box)

        # TOOLBAR
        toolbox = activity.ActivityToolbox(self)
        toolbox.show()

        toolbar = AnalizeToolbar(self)
        toolbox.add_toolbar(_('Interfaces'), toolbar)
        toolbar.show()

        self.set_toolbox(toolbox)
        self.show()

        # Dirty hide()
        toolbar = toolbox.get_activity_toolbar()
        toolbar.share.hide()
        toolbar.keep.hide()
    
    def switch_to_presence(self):
        self._clean_box()
        self._box.pack_start(self._ps)

    def switch_to_xserver(self):
        self._clean_box()
        self._box.pack_start(self._xserver)

    def switch_to_network(self):
        self._clean_box()
        self._box.pack_start(self._network)

    def _clean_box(self):
        childs = self._box.get_children()
        for c in childs:
            self._box.remove(c)

class AnalizeToolbar(gtk.Toolbar):
    def __init__(self, handler):
        gtk.Toolbar.__init__(self)
        self._handler = handler

        network = ToolButton('network-wireless-060')
        network.set_tooltip(_('Network Status'))
        network.connect('clicked', self._on_network_clicked_cb)
        self.insert(network, -1)
        network.show()

        xserver = ToolButton('dialog-cancel')
        xserver.set_tooltip(_('X Server'))
        xserver.connect('clicked', self._on_xserver_clicked_cb)
        self.insert(xserver, -1)
        xserver.show()

        presence = ToolButton('computer-xo')
        presence.set_tooltip(_('Presence Service'))
        presence.connect('clicked', self._on_presence_clicked_cb)
        self.insert(presence, -1)
        presence.show()

    def _on_presence_clicked_cb(self, widget):
        self._handler.switch_to_presence()

    def _on_xserver_clicked_cb(self, widget):
        self._handler.switch_to_xserver()

    def _on_network_clicked_cb(self, widget):
        self._handler.switch_to_network()
