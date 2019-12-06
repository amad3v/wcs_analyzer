import sys
from pathlib import Path
# from mods import fixqt
from PyQt5.QtWidgets import QMessageBox


class EmptyList(Exception):
    pass


class NoTargetFile(Exception):
    pass


def report_feedback(title, text, icon=1, parent=None):
    # icon values:
    # QMessageBox.Information = 1
    # QMessageBox.Warning = 2
    box = QMessageBox()
    box.setText(text)
    box.setWindowTitle(title)
    box.setParent(parent)
    box.setIcon(icon)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec_()


def get_error_details():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    # linecache.checkcache(filename)
    # line = linecache.getline(filename, lineno, f.f_globals)
    # print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(Path(filename).name, lineno, line.strip(), exc_obj))
    return 'In: {0} ({1})\n{2}:\n{3}'.format(str(Path(filename).stem), str(lineno), exc_type, exc_obj)
