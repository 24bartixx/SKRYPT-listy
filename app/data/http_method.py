from enum import Enum

class HTTP_method(Enum):
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PUT = "PUT"
    DELETE = "DELETE"
    POST = "POST"
    PATCH = "PATCH"
    CONNECT = "CONNECT"
    PROPFIND = "PROPFIND"
    SEARCH = "SEARCH"
    DESCRIBE = "DESCRIBE"
    TRACK = "TRACK"
    RPC_CONNECT = "RPC_CONNECT"
    UNSPECIFIED = "-"
    UNKNOWN = "UNKNOWN"