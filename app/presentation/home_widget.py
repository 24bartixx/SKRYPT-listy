import os
from datetime import timezone
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QListView, QLabel, QDateTimeEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QItemSelectionModel
from app.data.read_log import read_log
from app.presentation.log_list_model import LogListModel
from app.data.http_indexes import Fields

class HomeWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = self.__load_ui()
        self.__fetch_widgets()
        self.__set_up_on_clicks()
        self.setCentralWidget(self.ui)
        self.setFixedSize(self.ui.size())
        
        self.data = None
        self.display_data = None
        self.current_index = None
        self.model =  None

    def __load_ui(self):
        loader = QUiLoader()
        file = QFile(os.path.join(os.path.dirname(__file__), "home.ui"))
        file.open(QFile.ReadOnly)
        widget = loader.load(file)
        file.close()
        return widget
    
    def __fetch_widgets(self):
        self.open_button = self.ui.findChild(QPushButton, "open_button")
        self.prev_button = self.ui.findChild(QPushButton, "previous_button")
        self.next_button = self.ui.findChild(QPushButton, "next_button")
        self.filter_button = self.ui.findChild(QPushButton, "filter_button")
        self.path = self.ui.findChild(QLineEdit, "search_bar")
        self.start_date = self.ui.findChild(QDateTimeEdit, "start_date")
        self.end_date = self.ui.findChild(QDateTimeEdit, "end_date")
        self.logs_list_view = self.ui.findChild(QListView, "log_list_view")
        self.timestamp = self.ui.findChild(QLabel, "timestamp")
        self.uid = self.ui.findChild(QLabel, "uid")
        self.source_ip = self.ui.findChild(QLabel, "source_ip")
        self.source_port = self.ui.findChild(QLabel, "source_port")
        self.server_ip = self.ui.findChild(QLabel, "server_ip")
        self.server_port = self.ui.findChild(QLabel, "server_port")
        self.http_method = self.ui.findChild(QLabel, "http_method")
        self.host = self.ui.findChild(QLabel, "host")
        self.uri = self.ui.findChild(QLabel, "uri")
        self.status_code = self.ui.findChild(QLabel, "status_code")
    
    def __set_up_on_clicks(self):
        self.open_button.clicked.connect(self.__get_new_data)
        self.filter_button.clicked.connect(self.__filter_data)
        self.logs_list_view.clicked.connect(self.__log_list_view_item_on_click)
        self.prev_button.clicked.connect(self.__prev_on_click)
        self.next_button.clicked.connect(self.__next_on_click)
        
    def __get_new_data(self):
        self.data = read_log(self.path.text())
        self.display_data = self.data
        self.model = LogListModel(self.display_data)
        self.logs_list_view.setModel(self.model)
        
    def __filter_data(self):
        if self.data:
            start = self.start_date.dateTime().toPython().replace(tzinfo=timezone.utc)
            end = self.end_date.dateTime().toPython().replace(tzinfo=timezone.utc)
            self.display_data = list(filter(
                lambda log: log[Fields.TIMESTAMP] >= start and log[Fields.TIMESTAMP] <= end,
                self.data
            ))
            self.__reset()
            self.model = LogListModel(self.display_data)
            self.logs_list_view.setModel(self.model)
            
        
    def __log_list_view_item_on_click(self, index):
        self.current_index = index.row()
        self.__populate_detail()
        
    def __prev_on_click(self):
        self.current_index -= 1
        self.__select_item()
        self.__populate_detail()
        
    def __next_on_click(self):
        self.current_index += 1
        self.__select_item()
        self.__populate_detail()
        
    def __populate_detail(self):
        if self.current_index is not None:
            log = self.model.get_item(self.current_index)
            self.timestamp.setText(log[Fields.TIMESTAMP].strftime("%Y-%m-%d %H:%M:%S"))
            self.uid.setText(log[Fields.UID])
            self.source_ip.setText(log[Fields.SOURCE_IP])
            self.source_port.setText(log[Fields.SOURCE_PORT])
            self.server_ip.setText(log[Fields.SERVER_IP])
            self.server_port.setText(log[Fields.SERVER_PORT])
            self.http_method.setText(log[Fields.METHOD])
            self.host.setText(log[Fields.HOST])
            self.uri.setText(log[Fields.URI])
            self.status_code.setText(log[Fields.STATUS_CODE])
        else:
            self.timestamp.setText("-")
            self.uid.setText("-")
            self.source_ip.setText("-")
            self.source_port.setText("-")
            self.server_ip.setText("-")
            self.server_port.setText("-")
            self.http_method.setText("-")
            self.host.setText("-")
            self.uri.setText("-")
            self.status_code.setText("-")
        
    def __select_item(self):
        index = self.model.index(self.current_index)
        print(type(index))
        self.logs_list_view.selectionModel().setCurrentIndex(
            index, QItemSelectionModel.SelectCurrent
        )
        self.logs_list_view.scrollTo(index)
    
    def __reset(self):
        self.current_index = None
        self.__populate_detail()
        