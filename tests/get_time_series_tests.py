
from other.get_time_series import *
from pathlib import Path
from datetime import datetime
import argparse
import timeit

CSV_DEFAULT_PATH = Path("data/measurements/2023_Hg(TGM)_1g.csv")

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
    
    test_function(get_time_series_transpose, path, should_test_getitem)
    test_function(get_times_series_list, path, should_test_getitem)
    test_function(get_time_series_deque, path, should_test_getitem)
    
    
if __name__ == "__main__":
    test()
                