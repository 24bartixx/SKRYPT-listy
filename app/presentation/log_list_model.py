from PySide6.QtCore import QAbstractListModel, Qt
from app.data.http_indexes import LOG_FIELD

class LogListModel(QAbstractListModel):
    def __init__(self, logs):
        super().__init__()
        self._logs = logs
        
    def rowCount(self, parent):
        return len(self._logs)
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._logs[index.row()].get(LOG_FIELD, "No data!")
        return None
    
    def get_item(self, index):
        return self._logs[index]
    