import os
from datetime import datetime, timezone
from ipaddress import ip_address
from app.data.http_indexes import *
from app.data.http_method import HTTP_method

def read_log(path = os.path.join(os.path.dirname(__file__), "http_first_100k.log")):
    with open(path, "r") as file:
        data = []
        for line in file:
            line_data = line.split("\t")
        
            # timestamp (UTC time)
            ts = datetime.fromtimestamp(float(line_data[LOG_INDEXES[Fields.TIMESTAMP]]), tz = timezone.utc)
            ts = ts.strftime("%Y-%m-%d %H:%M:%S")
            
            # uid 
            uid = line_data[LOG_INDEXES[Fields.UID]]

            # source ip
            source_ip = line_data[LOG_INDEXES[Fields.SOURCE_IP]]
            # try:
            #     source_ip = ip_address(line_data[LOG_INDEXES[Fields.SOURCE_IP]])
            # except ValueError:
            #     source_ip = line_data[LOG_INDEXES[Fields.SOURCE_IP]]
            
            # source port
            source_port = line_data[LOG_INDEXES[Fields.SOURCE_PORT]]
            # try:
            #     source_port = int(line_data[LOG_INDEXES[Fields.SOURCE_PORT]])
            # except ValueError:
            #     source_port = line_data[LOG_INDEXES[Fields.SOURCE_PORT]]
            
            # server ip
            server_ip = line_data[LOG_INDEXES[Fields.SERVER_IP]]
            # try:
            #     server_ip = ip_address(line_data[LOG_INDEXES[Fields.SERVER_IP]])
            # except ValueError:
            #     server_ip = line_data[LOG_INDEXES[Fields.SERVER_IP]]
                
            # server port
            server_port = line_data[LOG_INDEXES[Fields.SERVER_PORT]]
            # try:
            #     server_port = int(line_data[LOG_INDEXES[Fields.SERVER_PORT]])
            # except ValueError:
            #     server_port = line_data[LOG_INDEXES[Fields.SERVER_PORT]]
            
            # status code
            status_code = line_data[LOG_INDEXES[Fields.STATUS_CODE]]
            # try:
            #     status_code = int(line_data[LOG_INDEXES[Fields.STATUS_CODE]])
            # except ValueError:
            #     status_code = line_data[LOG_INDEXES[Fields.STATUS_CODE]]
        
            # HTTP method 
            method = line_data[LOG_INDEXES[Fields.METHOD]]
            # try:
            #     method = HTTP_method(line_data[LOG_INDEXES[Fields.METHOD]])
            # except ValueError:
            #     method = HTTP_method.UNKNOWN
                
            # host
            host = line_data[LOG_INDEXES[Fields.HOST]]
            # try:
            #     host = ip_address(line_data[LOG_INDEXES[Fields.HOST]])
            # except ValueError: 
            #     host = line_data[LOG_INDEXES[Fields.HOST]]

            uri = line_data[LOG_INDEXES[Fields.URI]]
            
            data_dict = {
                LOG_FIELD : line.replace("\t", " ")[:35] + "...",
                Fields.TIMESTAMP : ts,
                Fields.UID : uid,
                Fields.SOURCE_IP : source_ip,
                Fields.SOURCE_PORT : source_port,
                Fields.SERVER_IP : server_ip,
                Fields.SERVER_PORT : server_port,
                Fields.METHOD : method,
                Fields.HOST : host,
                Fields.URI : uri,
                Fields.STATUS_CODE : status_code,
            }
            
            data.append(data_dict)
            
        return data