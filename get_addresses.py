from utils import *
from read_data import read_metadata
import csv
import re
import sys


log = logger()


# common
def add_station(stations, match, voivodeship, city):
    
    if match:
        stations.append((
            voivodeship,
            city,
            match.group(1).strip(),
            match.group(2) if match.group(2) else None
        ))
    else:
        stations.append((
            voivodeship,
            city,
            None, None
            # station[METADATA_ADDRESS_PL], None      # if we want have sth if it doesn't match we can use this instead
        ))


def get_addresses(city, path = METADATA_FILE_PATH):
    
    stations = []
    metadata = read_metadata(path)
    
    for station in metadata[METADATA_STATIONS]:
        
        if city == station[METADATA_CITY_PL]:
            match = re.compile(ADDRESS_PATTERN).search(station[METADATA_ADDRESS_PL])
            add_station(stations, match, station[METADATA_VOIVODESHIP_PL], station[METADATA_CITY_PL])
                     
    return stations


def get_addresses_quicker(city, path = METADATA_FILE_PATH):
    
    stations = []
        
    if path.exists() and path.is_file() and path.suffix == ".csv":
        with open(path, "r", encoding = "utf-8") as file:
            reader = csv.reader(file)
                
            next(reader)
            
            for station in reader:
                if station[CITY_INDEX] == city:
                    match = re.compile(ADDRESS_PATTERN).search(station[ADRESS_INDEX])
                    add_station(stations, match, station[VOIVODESHIP_INDEX], station[CITY_INDEX],)
                    
    return stations


def main():
    
    city = DEFAULT_CITY
    if len(sys.argv) > 1:
        city = sys.argv[1]
        
    print ("\n===== ON THE FLY =====")
    for address in get_addresses_quicker(city):
        print("\t", address)
    
    print ("\n===== USING PROCESSED DATA =====")
    for address in get_addresses(city):
        print("\t", address)
        
    print()
    

if __name__ == "__main__":
    main()
    