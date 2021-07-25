# DONE:
# 1. Table of active serial ports added
#       (device name, port, status(?))
# 2. Check if added port already in table, if not add,
#    if exist then warn user

# TO DO:
# 1. Connect to specified port when port added to main table
# 2. Remove port from table if disconnected


# Sys modules
import sys,os

# Project modules
from Modules.ThreadWithReturn import ThreadWithReturn
from Modules.SerialParser import SerialParser
from Modules.Logger import Logger
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QTableWidget, QWidget, QGridLayout
from PyQt5.QtWidgets import QComboBox, QPushButton, QTableWidgetItem, QLabel
from PyQt5.QtCore import Qt

WINDOW_W = 1000
WINDOW_H = 700

THREADS = []
DEVICES = []
NUM_OF_ARDUINOS = 5
BAUDRATE = 9600

def initSystem():
    for i in range(NUM_OF_ARDUINOS):
        new_port = f"/dev/ttyACM{i}"
        new_device = SerialParser(port=new_port, baudrate=BAUDRATE)

        if new_device.isOpen():
            DEVICES.append( Logger(new_device, f"logfile{1+i}.txt", "w") )
            THREADS.append( ThreadWithReturn(target=DEVICES[i].logData) )

    for thread,_ in enumerate(THREADS):
        print(f"Thread {THREADS[thread]} starting")
        THREADS[thread].start()

    for thread,_ in enumerate(THREADS):
        print(f"Log data returned: {len(THREADS[thread].join())} characters")


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        # ATTRIBUTES
        self.CONNECTED_PORTS = []
        self.MAIN_TABLE_DATA = {
            'Device' : [],
            'Port' : self.CONNECTED_PORTS,
            'Status' : []
        }
        self.TABLE_COLUMNS = 3
        self.TABLE_ROWS = 0     # This is dynamic


        super().__init__(*args, **kwargs)
        # Init main window widget 
        self.setWindowTitle("Multi Threaded Serial Port Listener")
        self.resize(WINDOW_W, WINDOW_H)

        # config main widget
        self.MainWidget = QWidget()
        self.MainWidgetLayout = QGridLayout()
        self.MainWidget.setLayout(self.MainWidgetLayout)

        # place the main widget in main window as central widget
        self.setCentralWidget(self.MainWidget)

        # Init all other UI
        self.initUI()
        self.show()

    def initUI(self) -> None:

        # Input dialog with combo box
        self.port_selection = QComboBox()
        self.port_selection.addItems(self.getPorts())

        # Port selection control buttons
        self.add_port_btn = QPushButton("Add")
        self.add_port_btn.clicked.connect(self.portAdded)

        self.refresh_port_btn = QPushButton("Refresh Ports")
        self.refresh_port_btn.clicked.connect(self.updatePorts)
        

        # Table view widget
        self.MAIN_TABLE = QTableWidget()
        self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
        self.MAIN_TABLE.setColumnCount(self.TABLE_COLUMNS)
        self.updateTableData()


        # Place all widget in main widget
        self.MainWidgetLayout.addWidget(self.MAIN_TABLE, 0, 0, 1, 3)
        self.MainWidgetLayout.addWidget(self.port_selection, 1, 0, 1, 2)
        self.MainWidgetLayout.addWidget(self.add_port_btn, 1, 2, 1, 1)
        self.MainWidgetLayout.addWidget(self.refresh_port_btn, 1, 3, 1, 1)

    def updateTableData(self): 
        horHeaders = []
        for col, key in enumerate(sorted(self.MAIN_TABLE_DATA.keys())):
            horHeaders.append(key)
            for row, item in enumerate(self.MAIN_TABLE_DATA[key]):
                newitem = QTableWidgetItem(item)
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

        if new_connection not in self.MAIN_TABLE_DATA["Port"]:
            self.CONNECTED_PORTS.append(new_connection)

            # Update table content
            self.TABLE_ROWS += 1
            self.MAIN_TABLE.setRowCount(self.TABLE_ROWS)
            self.updateTableData()
        else:
            # Dialog box
            MainWindow.showDialog("WARNING","Cannot assign already existing port.")
            pass


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
