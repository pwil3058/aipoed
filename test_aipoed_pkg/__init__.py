### -*- coding: utf-8 -*-
###
###  test_aipoed_pkg.__init__.py
###
###  Copyright 2016 Peter Williams <pwil3058@gmail.com>
###
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
import gettext

APP_NAME = "test_aipoed"
BUG_TRACK_URL = "https://github.com/pwil3058/aipoed/issues"
DISCUSSION_GRP = "pwil3058@gmail.com"
CONFIG_DIR_PATH = os.path.expanduser(os.path.join("~", ".config", APP_NAME))

if not os.path.exists(CONFIG_DIR_PATH):
    os.makedirs(CONFIG_DIR_PATH)

from aipoed import i18n

LOCALE_DIR = i18n.find_locale_dir()

gettext.install(APP_NAME, localedir=LOCALE_DIR)
