# Fields
LOG_FIELD = "log"

class Fields:
    TIMESTAMP = "ts"
    UID = "uid"
    SOURCE_IP = "id.orig_h"
    SOURCE_PORT = "id.orig_p"
    SERVER_IP = "id.resp_h"
    SERVER_PORT = "id.resp_p"
    METHOD = "method"
    HOST = "host"
    URI = "uri"
    STATUS_CODE = "status_code"
    
# Log indexes
LOG_INDEXES = {
    Fields.TIMESTAMP: 0,
    Fields.UID: 1,
    Fields.SOURCE_IP: 2,
    Fields.SOURCE_PORT: 3,
    Fields.SERVER_IP: 4,
    Fields.SERVER_PORT: 5,
    Fields.METHOD: 7,
    Fields.HOST: 8,
    Fields.URI: 9,
    Fields.STATUS_CODE: 14
}