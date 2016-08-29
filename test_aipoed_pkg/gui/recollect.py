### -*- coding: utf-8 -*-
###
###  aipoed/gui/recollect.py
###
### Copyright (C) 2010-2016 Peter Williams <pwil3058@gmail.com>
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

'''Remember stuff for the GUI. Sizes, positions, etc.'''

from aipoed.gui import recollect
from aipoed.gui.recollect import define, set, get, Defn

from .. import CONFIG_DIR_PATH, APP_NAME

recollect.initialize(CONFIG_DIR_PATH)

define(APP_NAME, "last_wd", Defn(str, ""))
