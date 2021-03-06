# DONEEEE:
# - Table of active serial ports added
#      (device name, port)
# - Check if added port already in table, if not then add,
#       if exist then warn user
# - Add input prompt to enter device name ("arduino", "ESP", etc)
# - Integrate backend with frontend GUI calls
# - Multiple device is able to log data concurrently using threads
# - If device disconnected, then remove from the table
# - All test case succeeded.
# - Cleanup done
# - Added baudrate selection functionality
# - Workaround getPorts() method done. Now this program works both for POSIX
#   compliants and windows based system

# TODO:
# - Write test case report (screenshot & terminal output)

import sys,os

from PyQt5.QtWidgets import QDialog, QLineEdit, QMainWindow
from PyQt5.QtWidgets import QApplication, QTableWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt, QTimer
from Modules.BackendHandler import Handler

# from WindowsNT
if os.name == 'nt':
    from serial.tools.list_ports_windows import comports

# Mac & Linux are POSIX compliant (UNIX like systems)
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports

else:
    raise ImportError("OS Platform not properly detected")


# For comparison, Arduino UNO max is about 115200 ~ 230400
# Some device with higher clocks are able to reach 460800
BAUDRATES = ['4800', '9600', '19200', '28800', '57600',
             '115200', '230400', '460800', '576000']

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        # ATTRIBUTES
        self.HANDLERS = {}
        self.DEVICES_NAME = []
        self.CONNECTED_PORTS = []
        self.LOGFILES_LIST = []
        self.MAIN_TABLE_DATA = {
            'Device'  : self.DEVICES_NAME,
            'Port'    : self.CONNECTED_PORTS,
            'Logfile' : self.LOGFILES_LIST,
        }
        self.TABLE_COLUMNS = len(self.MAIN_TABLE_DATA.keys())
        self.TABLE_ROWS = 0

        super().__init__(*args, **kwargs)

        # Init main window widget 
        self.setWindowTitle("Multi Threaded Serial Port Listener")

        # config main widget
        self.MainWidget = QWidget()
        self.MainWidgetLayout = QGridLayout()
        self.MainWidget.setLayout(self.MainWidgetLayout)

        # place the main widget in main window as central widget
        self.setCentralWidget(self.MainWidget)

        # Init all other UI
        self.initUI()
        self.adjustSize()
        self.show()

        self.initTimer()

    def initUI(self):

        # Port selection
        self.port_selection = QComboBox()
        self.port_selection.addItems(self.getPorts())

        # baudrate selection
        self.baud_selection = QComboBox()
        self.baud_selection.addItems(BAUDRATES)

        # Input text
        self.input_device_name = QLineEdit()
        self.input_logfile_name = QLineEdit()

        # Labels
        self.in_device_label = QLabel("Device: ")
        self.in_logfile_name = QLabel("Logfile: ")
        self.in_baud_label = QLabel("Baudrate: ")
        

        # control buttons
        self.refresh_port_btn = QPushButton("Refresh Ports")
        self.refresh_port_btn.clicked.connect(self.updatePorts)
        
        self.add_port_btn = QPushButton("Add")
        self.add_port_btn.clicked.connect(self.portAdded)

        # Table view widget
        self.MAIN_TABLE = QTableWidget()
        self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
        self.MAIN_TABLE.setColumnCount(self.TABLE_COLUMNS)
        self.MAIN_TABLE.showNormal()
        self.updateTableData()

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateAll)
        self.timer.start(2)

        # Place all widget in main widget
        self.MainWidgetLayout.addWidget(self.MAIN_TABLE, 0, 0, 5, 4)
        self.MainWidgetLayout.addWidget(self.port_selection, 6, 0, 1, 1)
        self.MainWidgetLayout.addWidget(self.refresh_port_btn, 6, 1, 1, 1)
        self.MainWidgetLayout.addWidget(self.add_port_btn, 6, 2, 1, 2)
        self.MainWidgetLayout.addWidget(self.in_device_label, 7, 0, 1, 1)
        self.MainWidgetLayout.addWidget(self.input_device_name, 7, 1, 1, 1)
        self.MainWidgetLayout.addWidget(self.in_logfile_name, 7, 2, 1, 1)
        self.MainWidgetLayout.addWidget(self.input_logfile_name, 7, 3, 1, 1)
        self.MainWidgetLayout.addWidget(self.in_baud_label, 8, 0, 1, 1)
        self.MainWidgetLayout.addWidget(self.baud_selection, 8, 1, 1, 1)

    def updateTableData(self): 
        self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
        horHeaders = []

        for col, key in enumerate(self.MAIN_TABLE_DATA.keys()):
            horHeaders.append(key)

            # Add new items with read only
            for row, item in enumerate(self.MAIN_TABLE_DATA[key]):

                newitem = QTableWidgetItem(item)
                newitem.setFlags(newitem.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.MAIN_TABLE.setItem(row, col, newitem)

        self.MAIN_TABLE.setHorizontalHeaderLabels(horHeaders)

    def getPorts(self) -> list:
        serial_objects = comports()
        total = len(serial_objects)

        active_ports = [serial_objects[idx].device for idx in range(total)]
        return active_ports

    # EVENT HANDLERS
    def updatePorts(self):
        connected_ports = self.getPorts()
        current_ports = [self.port_selection.itemText(i) for i in range(self.port_selection.count())]
        new_port = []
        for port in connected_ports:
            if port not in current_ports:
                new_port.append(port)

        self.port_selection.addItems(new_port)

    def portAdded(self):
        # Update connected port list
        new_connection = self.port_selection.currentText()
        new_device = self.input_device_name.text()
        new_logfile = self.input_logfile_name.text()
        new_baud = int(self.baud_selection.currentText())

        # Check if new connection is already in table
        if new_connection not in self.MAIN_TABLE_DATA["Port"]:

            # Check if logfile & device nickname is specified
            if (len(new_device) > 0) and (len(new_logfile) > 0):
                
                # Try to connect
                new_handler = Handler(new_connection, new_logfile, new_baud)

                if new_handler.isActive():
                    self.DEVICES_NAME.append(new_device)
                    self.CONNECTED_PORTS.append(new_connection)
                    self.LOGFILES_LIST.append(new_logfile)
                    self.HANDLERS[new_connection] = new_handler
                    self.HANDLERS[new_connection].handleData()

                    # Update table content
                    self.TABLE_ROWS += 1
                    self.updateTableData()
                    self.adjustSize()
                else:
                    MainWindow.showDialog("ERROR", f"Cannot connect to {new_connection}")
            else:
                MainWindow.showDialog("ERROR", "Missing information. Please provide both logfile & device name")
        else:
            MainWindow.showDialog("ERROR","Cannot assign already existing port.")

        # Clear text
        self.input_device_name.setText('')
        self.input_logfile_name.setText('')

    def updateAll(self):
        inactive = []
        handler_keys = list(self.HANDLERS.keys())

        if len(handler_keys) > 0:
            for key in handler_keys:
                # remove handler if inactive
                if not self.HANDLERS[key].logger.is_active:
                    self.HANDLERS.pop(key, "")
                    inactive.append(key)

        # Remove corresponding table element
        for port in inactive:
            print(f"[LOGGER] {port} disconnected")
            index = self.CONNECTED_PORTS.index(port)
            self.CONNECTED_PORTS.pop(index)
            self.LOGFILES_LIST.pop(index)
            self.DEVICES_NAME.pop(index)

            self.TABLE_ROWS -= 1
            self.updateTableData()


    # Generic Dialog
    @staticmethod
    def showDialog(dialog_title:str, msg:str):
        d = QDialog()
        layout = QGridLayout()
        d.setLayout(layout)

        warn_msg = QLabel(msg)
        layout.addWidget(warn_msg,0,0)

        d.setWindowTitle(dialog_title)
        d.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    exit(app.exec_())
