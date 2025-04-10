from pathlib import Path
import logging
import sys

# paths
DATA_CATALOG = Path("./data")
MEASUREMENTS_CATALOG = DATA_CATALOG / "measurements"
RESULT_CATALOG = Path("D:/Dummy/")
DATA_RESULT_PATH = RESULT_CATALOG / "read.json"
METADATA_FILE_PATH = DATA_CATALOG / "stacje.csv"
MEASUREMENTS_RESULT_PATH = RESULT_CATALOG / "measurements.json"

# ex 1 (read_data)
METADATA_RESULT_PATH = RESULT_CATALOG / "metadata.json"
METADATA_STATIONS = "stations"

MEASUREMENTS_MEASUREMENTS = "measurements"
MEASUREMENTS_STATION_CODE = "station code"
MEASUREMENTS_INDICATOR = "indicator"
MESAUREMENTS_AVERAGING_TIME = "averaging time"
MEASUREMENTS_UNIT = "unit"
MEASUREMENTS_POSITION_CODE = "position_code"
MEASUREMENTS_TIME = "time"
MEASUREMENTS_VALUE = "value"
MEASUREMENTS_YEAR = "time"

# ex 2
KEY_TUPLE_PATTERN = r"(\d{4})_(.+)_(.+).csv"

# ex 3
DEFAULT_CITY = "Wrocław"

VOIVODESHIP_INDEX = 10
CITY_INDEX = 11
ADRESS_INDEX = 12

ADDRESS_PATTERN = r"^(.*?)\s*(\d+[a-zA-Z]?([/-]\d+)?)?$"

#   ^ - starts with
#   (.*?) 
#       group(1), 
#       . - any character, 
#       *? - "lazy quantifier" jak najmniej aby dopasowanie się udało
#   \s* - spaces in between
#   (\d+[a-zA-Z]?([/-]\d+)?)? - opcjonalnie numer
#       group(2)
#       \d+ - cyfry (1+)
#       [a-zA-Z]? - opcjonalnie litera
#       ([/-]\d+)? 
#           group(3) - opcjonalna część numeru
#           [/-] - ukośnik lub myślnik
#           \d+ - cyfry (1+)
#   $ - koniec regexa


# ex 4 (patters)
DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"
COORDS_PATTERN = r"\d{2}\.\d{6}"
TWO_COMPARTMENTS_PATTERN = r"\s*\S+\s*-\s*\S+\s*"
MOB_PATTERN = r".*MOB\s*"
MOBILE_PATTERN = r".*mobilna.*"
THREE_COMPARTMENTS_PATTERN = r"\s*\S+\s*-\s*\S+\s*-\s*\S+\s*"
UL_AL_PATTERN = r"(?:ul\.|al\.).*,.*"

# ex 4 (column names)
METADATA_CODE_STATION_PL = "Kod stacji"         # ex1
METADATA_STATION_NAME_PL = "Nazwa stacji"       # ex1
METADATA_STATION_TYPE_PL = "Rodzaj stacji"
METADATA_VOIVODESHIP_PL = "Województwo"
METADATA_CITY_PL = "Miejscowość"                # ex1
METADATA_ADDRESS_PL = "Adres"                   # ex1
METADATA_LATITUDE = "WGS84 φ N"
METADATA_LONGITUDE = "WGS84 λ E"
METADATA_OPEN_DATE_PL = "Data uruchomienia"
METADATA_CLOSURE_DATE_PL = "Data zamknięcia"

# ex 4 (convert)
POLISH_CHARS_TO_LATIN_AND_SPACE = {
    'ą': 'a',
    'ć': 'c',
    'ę': 'e',
    'ł': 'l',
    'ń': 'n',
    'ó': 'o',
    'ś': 's',
    'ź': 'z',
    'ż': 'z',
    'Ą': 'A',
    'Ć': 'C',
    'Ę': 'E',
    'Ł': 'L',
    'Ń': 'N',
    'Ó': 'O',
    'Ś': 'S',
    'Ź': 'Z',
    'Ż': 'Z',
    " ": "_"        # space to underscore
}


# ex 5+
COMMAND = "command"
COMMAND_RANDOM = "random"
COMMAND_STATION = "station"
COMMAND_ANOMALIES = "anomalies"

RANDOM_NAME = "name"
RANDOM_CITY = "city"
RANDOM_ADDRESS = "address"

ANOMALIES_CHANGE = "change"
ANOMALIES_INCORRECT = "incorrect"
ANOMALIES_TOO_HIGH = "too_high"
ANOMALIES_THRESHOLD = "alarm_threshold"

ANOMALIES = {
   ("SO2", "24g"): {
       ANOMALIES_CHANGE: 2.0,
       ANOMALIES_THRESHOLD: 3.8
   } 
}




def logger(name = "logger"):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda log: log.levelno < logging.WARNING)
        stdout_handler.setFormatter(logging.Formatter("%(levelname)s\t%(message)s"))
        logger.addHandler(stdout_handler)
        
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(logging.Formatter("%(levelname)s\t%(message)s"))
        logger.addHandler(stderr_handler)
    
    return logger


class A:
    def __init__(self, x):
        self.x = x
        
class B:
    def __init__(self, x):
        self.x = x
        
        
class C(A,B):
    def __init__(self, x):
        A.__init__(self, x)
        B.__init__(self, x)
        
c = C(4)

c.x