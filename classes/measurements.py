import csv
import itertools
from itertools import chain
from other.get_time_series import get_time_series_transpose
from classes.series_validators import *


class Measurements:
    
    def __init__(self, catalog_path):
        self.catalog_path = catalog_path
        self.data_paths = self.__get_data_paths()
    
        
    def __get_data_paths(self):
        
        data_paths = {}
    
        for csv_path in filter(lambda path: path.is_file() and path.suffix == ".csv", self.catalog_path.iterdir()):
            data_paths[csv_path] = None
            
        return data_paths


    def __file_contains(self, path, key_word, index):
        
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            
            for i in range(index):
                next(reader)
                
            if key_word in next(reader)[1:]:
                return True
                    
        return False
    
        
    # i.
    def __len__(self):
        
        time_series_count = sum(len(series) for series in self.data_paths.values() if series)
        
        for path, time_series in self.data_paths.items():
            if not time_series:
                with open(path, "r", encoding = "utf-8") as file:
                    reader = csv.reader(file)
                    time_series_count += len(next(reader)) - 1
                
        return time_series_count
    
    
    # ii.
    def  __contains__(self, parameter_name: str):
    
        # IMPLEMENTATION 1 -> using names of files
        # for path in self.data_paths:
        #     if parameter_name in str(path):
        #         return True
        # return False
        
        # IMPLEMENTATION 2 -> exploring content of the files
        for _, time_series in self.data_paths.items():
            if time_series and time_series.indicator == parameter_name:
                return True
            
        for path, time_series in self.data_paths.items():
            if not time_series and self.__file_contains(path, parameter_name, 2):
                return True
                    
        return False
        
        
    def __get_by(self, series_attr_name, attr_value, attr_index):
        
        result_time_series_list = []
        
        for path, time_series_list in self.data_paths.items():
            if time_series_list:
                result_time_series_list += [series for series in time_series_list if getattr(series, series_attr_name) == attr_value]
            else:
                if self.__file_contains(path, attr_value, attr_index):
                    parsed_time_series_list = get_time_series_transpose(path)
                    self.data_paths[path] = parsed_time_series_list
                    result_time_series_list += [series for series in parsed_time_series_list if getattr(series, series_attr_name) == attr_value]
        
        return result_time_series_list
        
        
    # iii.
    def get_by_parameter(self, param_name: str):
        return self.__get_by("indicator", param_name, 2)
    
    
    # iv.
    def get_by_station(self, station_code: str):
        return self.__get_by("station_code", station_code, 1)
    
    
    def detect_all_anomalies(self, validators: list[SeriesValidator], preload: bool = False):
        anomalies = {}

        for validator in validators:
            validator_name = validator.__class__.__name__
            anomalies[validator_name] = []

            for path, time_series_list in self.data_paths.items():
                if time_series_list:
                    for series in time_series_list:
                        for message in validator.analyze(series):
                            anomalies[validator_name].append(message)
                elif preload:
                    parsed_time_series_list = get_time_series_transpose(path)
                    self.data_paths[path] = parsed_time_series_list
                    for series in parsed_time_series_list:
                        for message in validator.analyze(series):
                            anomalies[validator_name].append(message)

        return anomalies