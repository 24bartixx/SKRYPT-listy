from datetime import datetime
from utils import logger

log = logger()

class Station:

    def __init__(self, *args):
        self.__number = args[0] if len(args) > 0 else None
        self.__station_code = args[1] if len(args) > 1 else None
        self.__international_code = args[2] if len(args) > 2 else None
        self.__name = args[3] if len(args) > 3 else None
        self.__old_station_code = args[4] if len(args) > 4 else None
        self.__open_date = self.__convert_to_date(args[5]) if len(args) > 5 else None
        self.__closure_date = self.__convert_to_date(args[6]) if len(args) > 6 else None
        self.__station_type = args[7] if len(args) > 7 else None
        self.__area_type = args[8] if len(args) > 8 else None
        self.__station_kind = args[9] if len(args) > 9 else None
        self.__voivodship = args[10] if len(args) > 10 else None
        self.__city = args[11] if len(args) > 11 else None
        self.__address = args[12] if len(args) > 12 else None
        self.__latitude = args[13] if len(args) > 13 else None
        self.__longitude = args[14] if len(args) > 14 else None

    def __convert_to_date(self, date):
        if not date:
            return None
        try:
            return datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            log.warning(f"Error: '{date}' is not in the correct format (YYYY-MM-DD)!")
            return date

    def __str__(self):
        return (
            f"Station code: {self.__station_code}\n"
            f"Station name: {self.__name}\n"
            f"Old station code: {self.__old_station_code}\n"
            f"Open date: {self.__open_date}\n"
            f"Closure date: {self.__closure_date}\n"
            f"Station type: {self.__station_type}\n"
            f"Area type: {self.__area_type}\n"
            f"Station kind: {self.__station_kind}\n"
            f"Voivodship: {self.__voivodship}\n"
            f"City: {self.__city}\n"
            f"Address: {self.__address}\n"
            f"Latitude: {self.__latitude}\n"
            f"Longitude: {self.__longitude}"
        )

    def __repr__(self):
        return (
            f"Station(number={self.__number}, station_code={self.__station_code}, international_code={self.__international_code}, "
            f"name={self.__name}, old_station_code={self.__old_station_code}, open_date={self.__open_date}, "
            f"closure_date={self.__closure_date}, station_type={self.__station_type}, area_type={self.__area_type}, "
            f"station_kind={self.__station_kind}, voivodship={self.__voivodship}, city={self.__city}, address={self.__address}, "
            f"latitude={self.__latitude}, longitude={self.__longitude})"
        )

    def __eq__(self, other):
        if isinstance(other, Station):
            return self.__station_code == other.__station_code
        return False
    