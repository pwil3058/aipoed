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

import os

from gi.repository import Gtk

from aipoed.decorators import singleton

from aipoed import enotify

from aipoed.gui import dialogue
from aipoed.gui import file_tree
from aipoed.gui import actions
from aipoed.gui import recollect
from aipoed.gui import terminal
from aipoed.gui import gutils
from aipoed.gui import icons
from aipoed.gui import console

from aipoed.patch_diff.gui import patch_view

from aipoed.patch_diff import patchlib

from aipoed.patch_diff.gui import patch_view

from .. import APP_NAME

from . import recollect

recollect.define("main_window", "last_geometry", recollect.Defn(str, ""))

@singleton
class MainWindow(dialogue.MainWindow, actions.CAGandUIManager, enotify.Listener):
    UI_DESCR = \
        """
        <ui>
            <menubar name="left_side_menubar">
                <menu action="working_directory_menu">
                    <menuitem action="change_wd_action"/>
                    <menuitem action="view_patch_action"/>
                    <menuitem action="quit_action"/>
                </menu>
            </menubar>
            <menubar name="right_side_menubar">
                <menu action="configuration_menu">
                    <menuitem action="allocate_xtnl_editors"/>
                    <menuitem action="config_auto_update"/>
                </menu>
            </menubar>
        </ui>
        """
    def __init__(self):
        dialogue.MainWindow.__init__(self)
        dialogue.BusyIndicator.__init__(self)
        actions.CAGandUIManager.__init__(self)
        enotify.Listener.__init__(self)
        vbox = Gtk.VBox()
        hbox = Gtk.HBox()
        self._lhs_menubar = self.ui_manager.get_widget("/left_side_menubar")
        self._rhs_menubar = self.ui_manager.get_widget("/right_side_menubar")
        hbox.pack_start(self._lhs_menubar, expand=True, fill=True, padding=0)
        hbox.pack_end(self._rhs_menubar, expand=False, fill=True, padding=0)
        vbox.pack_start(hbox, expand=False, fill=True, padding=0)
        vbox.pack_start(file_tree.FileTreeWidget(), expand=True, fill=True, padding=0)
        if terminal.AVAILABLE:
            vbox.pack_start(terminal.Terminal(), expand=True, fill=True, padding=0)
        vbox.pack_start(console.LOG, expand=True, fill=True, padding=0)
        vbox.pack_start(BITester(), expand=False, fill=True, padding=0)
        vbox.pack_start(AskerTester(), expand=False, fill=True, padding=0)
        vbox.pack_start(AskerResponseTester(), expand=False, fill=True, padding=0)
        self.add(vbox)
        self.connect("destroy", lambda _widget: Gtk.main_quit())
        self.connect("configure_event", self._configure_event_cb)
        self.parse_geometry(recollect.get("main_window", "last_geometry"))
        self.show_all()
        self._update_title()
        self.add_notification_cb(enotify.E_CHANGE_WD, self._reset_after_cd)
        pvw = patch_view.PatchWidget(patchlib.Patch.parse_text(""), "empty patch")
    def populate_action_groups(self):
        self.action_groups[actions.AC_DONT_CARE].add_actions(
            [
                ("working_directory_menu", None, _("_Working Directory")),
                ("configuration_menu", None, _("_Configuration")),
                ("change_wd_action", Gtk.STOCK_OPEN, _("_Open"), "",
                 _("Change current working directory"), self._change_wd_acb),
                ("view_patch_action", Gtk.STOCK_OPEN, _("View Patch"), "",
                 _("View a patch file"), self._view_patch_acb),
                ("quit_action", Gtk.STOCK_QUIT, _("_Quit"), "",
                 _("Quit"), lambda _action : Gtk.main_quit()),
            ])
    def _update_title(self):
        self.set_title(APP_NAME + ": ~{0}".format(os.path.relpath(os.getcwd(), os.getenv("HOME"))))
    def _reset_after_cd(self, *args, **kwargs):
        with self.showing_busy():
            self._update_title()
    def _change_wd_acb(self, _action=None):
        new_dir_path = self.ask_dir_path("New Directory Path", suggestion=None, existing=True)
        if new_dir_path and os.path.isdir(new_dir_path):
            with self.showing_busy():
                result = os.chdir(new_dir_path)
                enotify.notify_events(enotify.E_CHANGE_WD)
                recollect.set(APP_NAME, "last_wd", os.getcwd())
    def _view_patch_acb(self, _action=None):
        patch_file_path = self.ask_file_path("Patch File Path:", existing=True)
        if patch_file_path and os.path.exists(patch_file_path):
            PatchFileDialog(patch_file_path).show()
    def _configure_event_cb(self, widget, event):
        recollect.set("main_window", "last_geometry", "{0.width}x{0.height}+{0.x}+{0.y}".format(event))

class BITester(Gtk.HBox, dialogue.BusyIndicatorUser):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self._label = Gtk.Label("0")
        start_button = Gtk.Button.new_with_label(_("Start Show Busy"))
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

class AskerResponseTester(Gtk.HBox, dialogue.AskerMixin):
    def __init__(self):
        Gtk.HBox.__init__(self)
        self._label = Gtk.Label("Response")
        ask_button = Gtk.Button.new_with_label(_("Ask For Response"))
        self.pack_start(self._label, expand=True, fill=True, padding=0)
        self.pack_start(ask_button, expand=False, fill=True, padding=0)
        ask_button.connect("clicked", self._ask_button_clicked_cb)
        self.show_all()
    def _ask_button_clicked_cb(self, button):
        from aipoed import Suggestion, ActionResult
        result = ActionResult.error("File already exists.") | (Suggestion.RENAME|Suggestion.OVERWRITE)
        answer = self.accept_suggestion_or_cancel(result, "Accept a Suggestion or Cancel")#, [Suggestion.OVERWRITE, Suggestion.SKIP])
        self._label.set_text(dialogue.response_str(answer))

class PatchFileDialog(dialogue.Dialog):
    AUTO_UPDATE_TD = gutils.TimeOutController.ToggleData("auto_update_toggle", _("Auto _Update"), _("Turn data auto update on/off"), Gtk.STOCK_REFRESH)
    def __init__(self, patch_file_path, *args, **kwargs):
        self._patch_file_path = patch_file_path
        if "title" not in kwargs:
            kwargs["title"] = _("Patch File: \"{0}\"").format(patch_file_path)
        dialogue.Dialog.__init__(self, *args, **kwargs)
        self._widget = patch_view.PatchWidget(patchlib.Patch.parse_text_file(patch_file_path), os.path.basename(patch_file_path))
        self.vbox.pack_start(self._widget, expand=True, fill=True, padding=0)
        self.refresh_action = Gtk.Action("patch_view_refresh", _("_Refresh"), _("Reread the patch file."), icons.STOCK_REFRESH_PATCH)
        self.refresh_action.connect("activate", self._update_display_cb)
        refresh_button = gutils.ActionButton(self.refresh_action)
        self.auc = gutils.TimeOutController(toggle_data=self.AUTO_UPDATE_TD, function=self._update_display_cb, is_on=False, interval=10000)
        self.action_area.pack_start(gutils.ActionCheckButton(self.auc.toggle_action), expand=True, fill=True, padding=0)
        self.action_area.pack_start(refresh_button, expand=True, fill=True, padding=0)
        self.add_buttons(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)
        self.connect("response", self._close_cb)
        self.show_all()
    def _close_cb(self, dialog, response_id):
        self.auc.toggle_action.set_active(False)
        dialog.destroy()
    def _update_display_cb(self, *args, **kwargs):
        with self.showing_busy():
            self._widget.set_patch(patchlib.Patch.parse_text_file(self._patch_file_path))
