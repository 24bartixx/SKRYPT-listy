import csv
from ..models.time_series import TimeSeries
from pathlib import Path
from datetime import datetime
from collections import deque
from utils import logger
import argparse
import timeit


CSV_DEFAULT_PATH = Path("data/csv/measurements/2023_Hg(TGM)_1g.csv")
log = logger()


def safe_parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%y %H:%M")
    except ValueError:
        return date_str


def time_series_list_from_csv1(csv_path):
    
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
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], transposed[0], transposed[i+1])
            for i in range(count)
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")


def time_series_list_from_csv2(csv_path):
    
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
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], measurements[0], measurements[i + 1])
            for i in range(len(station_codes))
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")
    
    
def time_series_list_from_csv3(csv_path):
    
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
            TimeSeries(station_codes[i], indicators[i], averaging_times[i], units[i], measurements[0], list(measurements[i + 1]))
            for i in range(len(station_codes))
        ]
            
        return series
            
    else:
        log.error(f"The path {csv} is not csv file!")
        raise FileNotFoundError(f"The path {csv} is not csv file.")
    
    
def print_result(result):
    print("===== FIRST =====")
    print(result[0])
    print("\n===== LAST =====")
    print(result[-1])
    
    

def test_function(function, csv_path = CSV_DEFAULT_PATH, should_test_getitem = False):
    result = function(csv_path)
    print_result(result)
    if should_test_getitem:
        test_getitem(result)
    time = timeit.timeit(lambda: function(csv_path), number=1)
    print(f"\033[33m\nExecution time: {time} seconds\033[0m\n")
    
    
def test_getitem(result):
    
    station1 = result[0]
    station3 = result[2]
    
    print("\n===== Test: Integer Index =====")
    print(f"\t{station1[0]}")
    print(f"\t{station1[4]}")
    print(f"\t{station3[0]}")
    print(f"\t{station3[4]}")
    
    print("\n===== Test: Slice =====")
    print(f"\t{station1[0:5]}")
    print(f"\t{station1[slice(2,10,2)]}")
    print(f"\t{station3[0:5]}")
    print(f"\t{station3[slice(2,10,2)]}")
    
    print("\n===== Test: datetime Index =====")
    test_date1 = datetime(2023, 1, 2)
    test_date2 = datetime(2023, 4, 24)
    print(f"\t{station1[test_date1]}")
    print(f"\t{station1[test_date2]}")
    print(f"\t{station3[test_date1]}")
    print(f"\t{station3[test_date2]}")
    

def get_args():
    parser = argparse.ArgumentParser(description="Test CSV parsers for TimeSeries data.")

    parser.add_argument("--path", type=str, help="Path to the csv file")
    parser.add_argument("--should_test_getitem", action="store_true", help="Whether the module should test __getitem__() of TimeSeries class")

    return parser.parse_args()
    
    
def test(should_test_getitem = False):
    
    args = get_args()
    
    path = Path(args.path) if args.path else CSV_DEFAULT_PATH
    should_test_getitem = args.should_test_getitem
    
    test_function(time_series_list_from_csv1, path, should_test_getitem)
    test_function(time_series_list_from_csv2, path, should_test_getitem)
    test_function(time_series_list_from_csv3, path, should_test_getitem)
    
    
if __name__ == "__main__":
    test()
                