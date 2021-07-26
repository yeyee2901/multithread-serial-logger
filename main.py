# DONE:
# - Table of active serial ports added
#      (device name, port, status(?))
# - Check if added port already in table, if not add,
#       if exist then warn user
# - Add input prompt to enter device name ("arduino", "ESP", etc) d
# - Integrate backend with frontend GUI calls

# TODO:
# - Check threads during runtime update (during QTimer update)
#       if still active continue, else remove from HANDLERS list & MAIN_TABLE

import sys,os
from PyQt5.QtWidgets import QDialog, QLineEdit, QMainWindow, QApplication, QTableWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt, QTimer

from Modules.BackendHandler import Handler


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        # ATTRIBUTES
        self.HANDLERS = {}
        self.CONNECTED_PORTS = []
        self.LOGFILES_LIST = []
        self.DEVICES_NAME = []
        self.MAIN_TABLE_DATA = {
            'Device' : self.DEVICES_NAME,
            'Port' : self.CONNECTED_PORTS,
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

    def initUI(self):

        # Port selection
        self.port_selection = QComboBox()
        self.port_selection.addItems(self.getPorts())

        # Input text
        self.input_device_name = QLineEdit()
        self.input_logfile_name = QLineEdit()

        # Labels
        self.in_device_label = QLabel("Device: ")
        self.in_logfile_name = QLabel("Logfile: ")
        

        # control buttons
        self.add_port_btn = QPushButton("Add")
        self.add_port_btn.clicked.connect(self.portAdded)

        self.refresh_port_btn = QPushButton("Refresh Ports")
        self.refresh_port_btn.clicked.connect(self.updatePorts)
        

        # Table view widget
        self.MAIN_TABLE = QTableWidget()
        self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
        self.MAIN_TABLE.setColumnCount(self.TABLE_COLUMNS)
        self.MAIN_TABLE.showNormal()
        self.updateTableData()


        # Place all widget in main widget
        self.MainWidgetLayout.addWidget(self.MAIN_TABLE, 0, 0, 5, 4)
        self.MainWidgetLayout.addWidget(self.port_selection, 6, 0, 1, 1)
        self.MainWidgetLayout.addWidget(self.refresh_port_btn, 6, 1, 1, 1)
        self.MainWidgetLayout.addWidget(self.add_port_btn, 6, 2, 1, 2)
        self.MainWidgetLayout.addWidget(self.in_device_label, 7, 0, 1, 1)
        self.MainWidgetLayout.addWidget(self.input_device_name, 7, 1, 1, 1)
        self.MainWidgetLayout.addWidget(self.in_logfile_name, 7, 2, 1, 1)
        self.MainWidgetLayout.addWidget(self.input_logfile_name, 7, 3, 1, 1)

    def updateTableData(self): 
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
        device_list = os.listdir("/dev/")
        isTTY = [f"/dev/{device}" for device in device_list if ("tty" in device)]
        return isTTY


    # EVENT HANDLERS
    def updatePorts(self):
        self.port_selection.addItems(self.getPorts())

    def portAdded(self):
        # Update connected port list
        new_connection = self.port_selection.currentText()
        new_device = self.input_device_name.text()
        new_logfile = self.input_logfile_name.text()

        # Check if new connection is in already in table
        if new_connection not in self.MAIN_TABLE_DATA["Port"]:

            # Check if logfile & device is specified
            if (len(new_device) > 0) and (len(new_logfile) > 0):
                
                # Try to connect
                new_handler = Handler(new_connection, new_logfile)

                if new_handler.isActive():
                    self.DEVICES_NAME.append(new_device)
                    self.CONNECTED_PORTS.append(new_connection)
                    self.LOGFILES_LIST.append(new_logfile)
                    self.HANDLERS[new_connection] = new_handler

                    # Start thread
                    self.HANDLERS[new_connection].start()
                    
                    # Update table content
                    self.TABLE_ROWS += 1
                    self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
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


    # Generic Dialog
    @staticmethod
    def showDialog(dialog_type, msg):
        d = QDialog()
        layout = QGridLayout()
        d.setLayout(layout)

        warn_msg = QLabel(msg)
        layout.addWidget(warn_msg,0,0)

        d.setWindowTitle(dialog_type)
        d.exec_()




if __name__ == "__main__":
    app = QApplication(sys.argv)

    main = MainWindow()

    exit(app.exec_())
