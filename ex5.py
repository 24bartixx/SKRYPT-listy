from read_data import read_measurements, read_metadata
from datetime import datetime
import random
import statistics
from utils import *

log = logger()


# helper
def get_station_code_from_name(station_name):
    
    stations_list = read_metadata(METADATA_FILE_PATH, should_log = True)[METADATA_STATIONS]
    
    return next(
        (station[METADATA_CODE_STATION_PL] for station in stations_list if station[METADATA_STATION_NAME_PL] == station_name), 
        None
    )
    
    
# helper
def get_values_in_range(measurements, start_date, end_date):
    
    first = len(measurements)
    last = -1
    
    start = 0
    end = len(measurements) - 1
    
    while start <= end:
        pivot = (start + end) // 2
        pivot_date = measurements[pivot][MEASUREMENTS_TIME].date()
        
        if pivot_date >= start_date:
            first = pivot
            end = pivot - 1
        else:
            start = pivot + 1
            
    start = 0
    end = len(measurements) - 1
    
    while start <= end:
        pivot = (start + end) // 2
        pivot_date = measurements[pivot][MEASUREMENTS_TIME].date()
        
        if pivot_date <= end_date:
            last = pivot
            start = pivot + 1
        else:
            end = pivot - 1
            
    if first <= last:
        return measurements[first:last+1]
    else: 
        return []

            
#random
def random_station_name(measurement, frequency, start, end):
    
    def is_within_dates(stations, start_date, end_date):
    
        if len(stations) <= 0:
            return False
    
        measurements = stations[0][MEASUREMENTS_MEASUREMENTS]
        
        start = 0
        end = len(measurements) - 1
        
        while start <= end:
            pivot = (start + end) // 2
            pivot_time = measurements[pivot][MEASUREMENTS_TIME].date()
            
            if start_date <= pivot_time <= end_date:
                return True
            if pivot_time > end_date:
                end = pivot - 1
            else: 
                start = pivot + 1
                
        return False
    
    data = read_measurements(MEASUREMENTS_CATALOG, should_log = True, filter_key = f"{measurement}_{frequency}")
    good_stations = []
    
    for stations in data[MEASUREMENTS_MEASUREMENTS].values():
        if is_within_dates(stations, start, end):
            for station in stations:
                good_stations.append(station[MEASUREMENTS_STATION_CODE])
                
    if len(good_stations) > 0:
        
        stations_list = read_metadata(METADATA_FILE_PATH, should_log = True)[METADATA_STATIONS]
        stations_list = [station for station in stations_list if station[METADATA_CODE_STATION_PL] in good_stations]
        
        if not stations_list:
            log.warning("No stations metadata matched filtered station codes.")
            return None
        
        random_station = random.choice(stations_list)
        
        return {
            RANDOM_NAME: random_station[METADATA_STATION_NAME_PL],
            RANDOM_CITY: random_station[METADATA_CITY_PL],
            RANDOM_ADDRESS: random_station[METADATA_ADDRESS_PL]
        }
        
    else:
        log.warning("No station found for given measurement, frequency, and dates!")
        return None


# station
def mean_and_standard_variation(measurement, frequency, start, end, station_name):
        
    def determine_decimal_points(some_list_of_floats):
        decimal_points = 0
        i = 0
        while i < len(some_list_of_floats) and i < 5:
            candidate = len(str(some_list_of_floats[i]).split(".")[1])
            if candidate > decimal_points:
                decimal_points = candidate
            i += 1

        return decimal_points
    
    data = read_measurements(MEASUREMENTS_CATALOG, should_log = True, filter_key = f"{measurement}_{frequency}")
    
    station_code = get_station_code_from_name(station_name)
    
    if station_code:
        
        measurements = []
        
        for stations in data[MEASUREMENTS_MEASUREMENTS].values():
            for station in stations:
                if station[MEASUREMENTS_STATION_CODE] == station_code:
                    
                    values = get_values_in_range(station[MEASUREMENTS_MEASUREMENTS], start, end)
                    values = [value[MEASUREMENTS_VALUE] for value in values] 
                    
                    if len(values) == 0:
                        log.warning(f"No {measurement} measurements for station {station_name} in given dates!")
                        
                    measurements += values
                    
        # measurements = [element for sublist in measurements for element in sublist]
        
        if len(measurements) == 0:
            log.warning("No measurements found for given measurement, frequency, and dates")
        
        return statistics.mean(measurements), statistics.stdev(measurements), determine_decimal_points(measurements)
        
    else:
        msg = f"Station with name {station_name} not found in metadata!"
        log.error(msg)
        raise ValueError(msg)
    
    
# anomalies
def anomalies(measurement, frequency, start, end, station_name):
        
    data = read_measurements(MEASUREMENTS_CATALOG, should_log = True, filter_key = f"{measurement}_{frequency}")
    
    station_code = get_station_code_from_name(station_name)
    
    if station_code:
        
        results = {}
        
        for file_name, stations in data[MEASUREMENTS_MEASUREMENTS].items():
            for station in stations:
                if station[MEASUREMENTS_STATION_CODE] == station_code:
                    
                    year = int(file_name[:4])
                    
                    results[year] = {
                        ANOMALIES_CHANGE: [],
                        ANOMALIES_INCORRECT: [],
                        ANOMALIES_TOO_HIGH: []
                    }
                    
                    max_change = ANOMALIES[(measurement, frequency)][ANOMALIES_CHANGE]
                    max_value = ANOMALIES[(measurement, frequency)][ANOMALIES_THRESHOLD]
                    
                    values = get_values_in_range(station[MEASUREMENTS_MEASUREMENTS], start, end)
                    
                    previous = None
                    
                    for i in range(1, len(values)):
                        
                        value = station[MEASUREMENTS_MEASUREMENTS][i][MEASUREMENTS_VALUE]
                        time = station[MEASUREMENTS_MEASUREMENTS][i][MEASUREMENTS_TIME]
                        
                        # change
                        if previous:
                            
                            value_yesterday = station[MEASUREMENTS_MEASUREMENTS][i-1][MEASUREMENTS_VALUE]
                            diff = value - value_yesterday
                            if value >= 0 and value_yesterday >= 0 and diff >= max_change:
                                results[year][ANOMALIES_CHANGE].append((
                                    station[MEASUREMENTS_MEASUREMENTS][i-1][MEASUREMENTS_TIME],
                                    time,
                                    diff
                                ))
                        
                        previous = values[i]
                        
                        # incorrect
                        if not value or value < 0:
                            results[year][ANOMALIES_INCORRECT].append((time, value))
                            
                        # too high
                        if value > max_value:
                            results[year][ANOMALIES_TOO_HIGH].append((time, value))
                    
        return results
    
    else:
        msg = f"Station with name {station_name} not found in metadata!"
        log.error(msg)
        raise ValueError(msg)
