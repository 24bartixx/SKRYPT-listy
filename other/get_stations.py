import csv
from ..classes.station import Station
from pathlib import Path
from logger import logger

log = logger()


def get_stations(csv_path = Path.cwd() / "data" / "csv" / "stacje.csv"):

    if csv_path.is_file() and csv_path.suffix == ".csv":
        
        stations = [] 
    
        with open(csv_path, "r", encoding = "utf-8") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for line in reader:
                log.debug("Adding station")
                stations.append(Station(*line))
                
        log.info(f"Parsed {len(stations)} stations!")
                
        return stations
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")
            
if __name__ == "__main__":
    get_stations()