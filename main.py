import ctypes
# import os (pathlib is used instead)
import linecache
import sys
from typing import Union, Any, List
from pathlib import Path, WindowsPath
import time

from mods import fixqt

# always import before PyQt5

# =======================================#
# the following is to make the app icon  #
# visible in the task bar                #
# =======================================#
if type(Path.home()) == WindowsPath:
    # if os.name == 'nt':
    app_id = 'mj.wcs_analyzer_17.gui.1.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
# =======================================#

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon
from mods.csvextractor import WCS
from mods.save_xl import DataToXL
from mods.params import Settings
from mods.err_report import *
from ui.mainwindow import Ui_mwWCS

# pathlib.WindowsPath, for posix OSs (linux, macOS) use PosixPath
# os.path.join(os.environ["HOMEPATH"], "Desktop")
# home = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# if os.name == 'posix':
#     home = os.path.expanduser("~/Desktop")
# if os.name == 'nt':
#     home = os.path.expanduser("~\\Desktop")
home = str(Path.home().joinpath('Desktop'))

# icon_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui"), "Icon.ico")
open_filter = "CSV files (*.csv)"
save_filter = "Excel Workbook (*.xlsx)"


def create_icon():
    try:
        app_icon = QIcon()

        full_path: Union[Path, Any] = Path('.').absolute().joinpath('ui')
        # os.path.join(os.path.dirname(os.path.realpath(__file__)), "ui")
        app_icon.addFile(str(full_path.joinpath('i16.png')), QtCore.QSize(16, 16))
        app_icon.addFile(str(full_path.joinpath('i24.png')), QtCore.QSize(24, 24))
        app_icon.addFile(str(full_path.joinpath('i32.png')), QtCore.QSize(32, 32))
        app_icon.addFile(str(full_path.joinpath('i48.png')), QtCore.QSize(48, 48))
        app_icon.addFile(str(full_path.joinpath('i128.png')), QtCore.QSize(12, 128))
        app_icon.addFile(str(full_path.joinpath('i256.png')), QtCore.QSize(256, 256))

        return app_icon
    except Exception:
        report_error("Error occurred (Icon)", get_error_details())


class MainWindow(QtWidgets.QMainWindow):  # window = qtw.QMainWindow()
    # def __init__(self, title="", mw_home="", op_filter="All files (*.*)", sv_filter="All files (*.*)", parent=None):
    def __init__(self, title="", op_filter="All files (*.*)", sv_filter="All files (*.*)", parent=None):
        super().__init__(parent)
        self.__title = title  # window.setWindowTitle("Student Manager")
        self.ui = Ui_mwWCS()  # ui_window = Ui_mwWCS()
        self.ui.setupUi(self)  # ui_window.setupUi(window)
        self.__target = Settings()  # mw_home
        self.__open_f = op_filter
        self.__save_f = sv_filter
        self.__excel_file = ""
        self.setWindowIcon(create_icon())  # QIcon(icon_path))
        self.__csv_files_list = []

    def __show_dialog(self):
        self.__csv_files_list, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files',
                                                                          self.__target.get_path('open'),
                                                                          self.__open_f)

        self.__csv_files_list = [str(Path(item)) for item in self.__csv_files_list]
        # for i in range(len(self.__csv_content_list)):
        # self.__csv_content_list[i]=str(Path(self.__csv_content_list[i]))
        # return QtWidgets.QFileDialog.getOpenFileNames(self, 'Open files', self.__target, self.__open_f)

    def on_add_clicked(self):
        # list_names = QtWidgets.QFileDialog(window, "Open files", home, "CSV files (*.csv)")
        # return (type List) contains:
        # 1. list of selected files, type: List
        # 2. filter (type str)
        # list_names, _ = self.__show_dialog()
        self.__show_dialog()
        self.ui.lstInput.addItems(self.__csv_files_list)
        if self.__csv_files_list:
            self.__target.set_path('open', self.__csv_files_list[-1])
            self.__target.save_settings()
        elif self.ui.lstInput.count():
            self.__csv_files_list = [self.ui.lstInput.item(i) for i in range(self.ui.lstInput.count())]

    def on_save_clicked(self):
        try:
            if len(self.__csv_files_list) == 0:
                raise EmptyList

            xl_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', self.__target.get_path('save'),
                                                               self.__save_f)

            if xl_file == '':
                raise NoTargetFile

            self.__target.set_path('save', xl_file)
            self.__target.save_settings()
            self.__excel_file = xl_file

            # y = time.process_time_ns()

            # Start timing
            # start = time.perf_counter()

            csv_wcs = WCS(self.__csv_files_list)

            boxes = csv_wcs.get_total_boxes()
            plates = csv_wcs.get_total_plates()
            total_exceptions = csv_wcs.get_total_exceptions()
            err_list = csv_wcs.get_list_count(1)
            rem_list = csv_wcs.get_list_count(0)
            status = csv_wcs.get_unique_list()

            # duration = time.perf_counter() - start
            # Timing stopped

            results = DataToXL(xl_file, total_exceptions, boxes, plates, status, err_list, rem_list)
            results.save_xl_file()

            report_task("File operation", "Excel file generated and saved\n" + str(Path(self.__excel_file)))
            # report_task("Execution time", str(
                # round(duration, 7)) + " seconds to:\nProcess 283 808 rows x 36 columns\nand 22 286 iterations in 47 files")
            # report_task("Execution time",
            #             str(round(duration, 7)) + " seconds to:\nProcess " + "{:,d}".format(boxes).replace(",", ' ') +
            #             " rows x 36 columns\nand " + "{:,d}".format(csv_wcs.loops).replace(",", ' ') + ' iteration')

        except NoTargetFile:
            report_error("Error occurred", "No target file!\nPlease enter file name")
        except EmptyList:
            report_error("Error occurred", "Empty list not allowed!\nPlease add CSV files")
        except Exception:
            report_error("Error occurred (SAVE)", get_error_details())

    def set_excel_file(self, file):
        self.__excel_file = file


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow("WCS Analyzer", open_filter, save_filter)
    window.ui.pbAdd.clicked.connect(window.on_add_clicked)
    window.ui.pbSave.clicked.connect(window.on_save_clicked)

    window.show()

    sys.exit(app.exec_())
