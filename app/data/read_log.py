from pathlib import Path
from datetime import datetime, timezone
from app.data.http_indexes import *

def read_log(path_str):
    path = Path(path_str)
    if not path.is_file() or path.suffix != ".log":
        raise FileNotFoundError(f"Path {path} is not a .log file!")
    
    with open(path, "r") as file:
        data = []
        for line in file:
            line_data = line.split("\t")
            
            data_dict = {
                LOG_FIELD : line.replace("\t", " ")[:35] + "...",
                Fields.TIMESTAMP : datetime.fromtimestamp(float(line_data[LOG_INDEXES[Fields.TIMESTAMP]]), tz = timezone.utc),
                Fields.UID : line_data[LOG_INDEXES[Fields.UID]],
                Fields.SOURCE_IP : line_data[LOG_INDEXES[Fields.SOURCE_IP]],
                Fields.SOURCE_PORT : line_data[LOG_INDEXES[Fields.SOURCE_PORT]],
                Fields.SERVER_IP : line_data[LOG_INDEXES[Fields.SERVER_IP]],
                Fields.SERVER_PORT : line_data[LOG_INDEXES[Fields.SERVER_PORT]],
                Fields.METHOD : line_data[LOG_INDEXES[Fields.METHOD]],
                Fields.HOST : line_data[LOG_INDEXES[Fields.HOST]],
                Fields.URI : line_data[LOG_INDEXES[Fields.URI]],
                Fields.STATUS_CODE : line_data[LOG_INDEXES[Fields.STATUS_CODE]]
            }
            
            data.append(data_dict)
            
        return data