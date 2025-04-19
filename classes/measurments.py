import csv
from itertools import chain
from ..other.get_time_series import get_time_series_transpose
from series_validators import *

class Measurements:
    
    def __init__(self, catalog_path):
        self.catalog_path = catalog_path
        self.paths = self.__get_csv_paths()
        self.time_series = []
        
        
    def __get_csv_paths(self):
        
        paths = {}
    
        for csv_path in filter(lambda path: path.is_file() and path.suffix == ".csv", self.catalog_path.iterdir()):
            paths[csv_path] = False
            
        return paths
        
    def __len__(self):
        
        time_series_count = len(self.time_series)
        
        for path, already_read in self.paths.items():
            if not already_read:
                with open(path, "r", encoding = "utf-8") as file:
                    reader = csv.reader(file)
                    time_series_count += len(next(reader)) - 1
                
        return time_series_count
    
    def  __contains__(self, parameter_name: str):
    
        for path in self.paths:
            if parameter_name in str(path):
                return True
            
        return False
    
    def __read_parameter(self, param_name):
        for path in self.paths:
            if not self.paths[path] and param_name in str(path):
                self.time_series += get_time_series_transpose(path)
                self.paths[path] = True
                
    def __read_data(self):
        self.time_series += list(chain.from_iterable(
            get_time_series_transpose(path) 
            for path, already_read in self.paths.items()
            if not already_read
        ))
        
    def get_by_parameter(self, param_name: str):
        self.__read_parameter(param_name)
        return [series for series in self.time_series if series.indicator == param_name]
    
    
    def get_by_station(self, station_code: str):
        self.__read_data()
        return [series for series in self.time_series if series.station_code == station_code]
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False):
        
        if preload:
            self.__read_data()
        
        anomalies = {}
        
        for validator in validators:
            messages = []
            for series in self.time_series:
                messages += validator.analyze(series)
            anomalies[validator.__class__.__name__] = messages
            