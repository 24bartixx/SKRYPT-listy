import csv
from classes.time_series import TimeSeries
from pathlib import Path
from datetime import datetime
from collections import deque
from other.logger import logger


log = logger()


def safe_parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%y %H:%M")
    except ValueError:
        return date_str
    
    
def safe_parse_float(value_str):
    try:
        return float(value_str)
    except ValueError:
        return value_str


def get_time_series_transpose(csv_path):
    
    if not isinstance(csv_path, Path):
        csv_path = Path(csv_path)

    if csv_path.is_file() and csv_path.suffix == ".csv":
        
        measurements = []
        
        with open(csv_path, "r", encoding = "utf-8") as file:
            reader = csv.reader(file)
            
            count = len(next(reader)) - 1
            station_codes = next(reader)[1:]
            indicators = next(reader)[1:]
            averaging_times = next(reader)[1:]
            units = next(reader)[1:]
            next(reader)
            
            for line in reader:
                measurements.append(line)
                
        transposed = [row for row in zip(*measurements)]
        
        transposed[0] = list(map(safe_parse_date, transposed[0]))
        
        series = [
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], transposed[0], list(map(safe_parse_float, transposed[i+1])))
            for i in range(count)
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")


def get_times_series_list(csv_path):
    
    if not isinstance(csv_path, Path):
        csv_path = Path(csv_path)

    if csv_path.is_file() and csv_path.suffix == ".csv":
        
        measurements = []
        
        with open(csv_path, "r", encoding = "utf-8") as file:
            reader = csv.reader(file)
            
            count = len(next(reader)) - 1
            station_codes = next(reader)[1:]
            indicators = next(reader)[1:]
            averaging_times = next(reader)[1:]
            units = next(reader)[1:]
            next(reader)
            
            measurements = [[] for _ in range(count + 1)]
            
            for line in reader:
                for i in range(count + 1):
                    measurements[i].append(line[i])
        
        measurements[0] = list(map(safe_parse_date, measurements[0]))
        
        series = [
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], measurements[0], list(map(safe_parse_float, measurements[i + 1])))
            for i in range(len(station_codes))
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")
    
    
def get_time_series_deque(csv_path):
    
    if not isinstance(csv_path, Path):
        csv_path = Path(csv_path)

    if csv_path.is_file() and csv_path.suffix == ".csv":
        
        measurements = deque()
        
        with open(csv_path, "r", encoding = "utf-8") as file:
            reader = csv.reader(file)
            
            count = len(next(reader)) - 1
            station_codes = next(reader)[1:]
            indicators = next(reader)[1:]
            averaging_times = next(reader)[1:]
            units = next(reader)[1:]
            next(reader)
            
            measurements = [deque() for _ in range(count + 1)]
            
            for line in reader:
                for i in range(count + 1):
                    measurements[i].append(line[i])
                    
        measurements[0] = list(map(safe_parse_date, measurements[0]))
        
        series = [
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], measurements[0], list(map(safe_parse_float, measurements[i + 1])))
            for i in range(len(station_codes))
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")
    
 