# Fix qt import error
# Include this file before import PyQt5

from logging import error  #logging
from os import path, environ, pathsep
import sys


def _append_run_path():
    if getattr(sys, 'frozen', False):
        # old code:
        # pathlist = []
        # pathlist.append(sys._MEIPASS)

        pathlist = [sys._MEIPASS]

        # If the application is run as a bundle, the pyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.

        # the application exe path
        _main_app_path = path.dirname(sys.executable)
        pathlist.append(_main_app_path)

        # append to system path environment
        environ["PATH"] += pathsep + pathsep.join(pathlist)

    error("current PATH: %s", environ['PATH'])


_append_run_path()
