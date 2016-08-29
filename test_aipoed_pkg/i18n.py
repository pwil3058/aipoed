### -*- coding: utf-8 -*-
###
###  test_aipoed_pgg/__init__.py
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

import gettext

from aipoed import i18n

from . import APP_NAME

LOCALE_DIR = i18n.find_locale_dir()

gettext.install(APP_NAME, localedir=LOCALE_DIR)
