### -*- coding: utf-8 -*-
###
###  Copyright (C) 2016 Peter Williams <pwil3058@gmail.com>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 of the License only.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from gi.repository import Gtk

from aipoed import singleton
from aipoed.gui import dialogue

from . import recollect

recollect.define("main_window", "last_geometry", recollect.Defn(str, ""))

@singleton
class MainWindow(dialogue.Window):
    def __init__(self):
        dialogue.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
        vbox = Gtk.VBox()
        vbox.pack_start(BITester(), expand=False, fill=True, padding=0)
        vbox.pack_start(AskerTester(), expand=False, fill=True, padding=0)
        self.add(vbox)
        self.connect("destroy", lambda _widget: Gtk.main_quit())
        self.parse_geometry(recollect.get("main_window", "last_geometry"))
        self.show_all()

class BITester(Gtk.HBox, dialogue.BusyIndicatorUser):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self._label = Gtk.Label("0")
        start_button = Gtk.Button.new_with_label(_("Start"))
        self.pack_start(self._label, expand=True, fill=True, padding=0)
        self.pack_start(start_button, expand=False, fill=True, padding=0)
        start_button.connect("clicked", self._start_button_clicked_cb)
        self.show_all()
    def _start_button_clicked_cb(self, button):
        button.set_sensitive(False)
        with self.showing_busy():
            for i in range(1000):
                self._label.set_text(str(i))
                dialogue.yield_to_pending_events()
        button.set_sensitive(True)

class AskerTester(Gtk.HBox, dialogue.AskerMixin):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self._label = Gtk.Label("Response")
        ask_button = Gtk.Button.new_with_label(_("Ask Question"))
        self.pack_start(self._label, expand=True, fill=True, padding=0)
        self.pack_start(ask_button, expand=False, fill=True, padding=0)
        ask_button.connect("clicked", self._ask_button_clicked_cb)
        self.show_all()
    def _ask_button_clicked_cb(self, button):
        answer = self.ask_question("A question that needs answering with OK or Cancel")#, "Elaboration would go here.")
        if answer == Gtk.ResponseType.OK:
            self._label.set_text("OK")
        else:
            self._label.set_text("Cancel")
