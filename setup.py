### -*- coding: utf-8 -*-
###
###  Copyright 2016 Peter Williams <pwil3058@gmail.com>
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

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import glob

here = path.abspath(path.dirname(__file__))

NAME = "aipoed"

DESCRIPTION = "A Python package provide application independent support for Peter Williams' GUI applications."

from aipoed import VERSION

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

pixmaps = glob.glob("pixmaps/*.png")

PIXMAPS = [("share/pixmaps/aipoed", pixmaps)]
print(PIXMAPS)

COPYRIGHT = [("share/doc/aipoed", ["COPYING", "copyright"])]

LICENSE = "GNU General Public License (GPL) Version 2.0"

CLASSIFIERS = [
    "Development Status :: Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: {}".format(LICENSE),
    "Programming Language :: Python",
    "Topic :: Software Development :: Tools",
    #"Operating System :: MacOS :: MacOS X",
    #"Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
]

KEYWORDS = []

AUTHOR = "Peter Williams"

AUTHOR_EMAIL = "pwil3058@gmail.com"

URL = "https://github.com/pwil3058/aipoed"

SCRIPTS = []

PACKAGES = find_packages(exclude=["pixmaps", "test_aipoed_pkg", "test_aipoed_pkg.gui"])

INSTALL_REQUIRES = []

EXTRAS_REQUIRE = {}

PACKAGE_DATA = {}

ENTRY_POINTS = {}

setup(
    name = NAME,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = VERSION,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    # The project's main homepage.
    url = URL,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = CLASSIFIERS,

    # Choose your license
    license = LICENSE,

    # Author details
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,

    # What does your project relate to?
    keywords = KEYWORDS,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages = PACKAGES,
    install_requires = INSTALL_REQUIRES,
    extras_require = EXTRAS_REQUIRE,

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data = PACKAGE_DATA,

    # Although "package_data" is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, "data_file" will be installed into "<sys.prefix>/my_data"
    data_files = PIXMAPS + COPYRIGHT,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts = SCRIPTS,
    entry_points = ENTRY_POINTS,
)
