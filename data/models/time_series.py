from datetime import datetime, date
from statistics import mean, stdev

class TimeSeries:
    def __init__(self, stations_code, indicator, averaging_time, unit, dates, values):
        self.__indicator = indicator
        self.__station_code = stations_code
        self.__averaging_time = averaging_time
        self.__unit = unit
        self.__dates = dates
        self.__values = values
        
    def __str__(self):
        return (
            "Station"
            f"\n\tIndicator: {self.__indicator}"
            f"\n\tStation code: {self.__station_code}"
            f"\n\tAveraging time: {self.__averaging_time}"
            f"\n\tUnit: {self.__unit}"
            f"\n\tFirst 5 dates: {[self.__dates[i] for i in range(3)]}"
            f"\n\tFirst 5 values: {[self.__values[i] for i in range(3)]}"
            f"\n\tLast 5 dates: {[self.__dates[i] for i in range(-3, 0)]}"
            f"\n\tLast 5 values: {[self.__values[i] for i in range(-3, 0)]}"
        )
        
    def __getitem__(self, param):
        
        if isinstance(param, int):
            if param < -len(self.__dates) or param >= len(self.__dates):
                raise IndexError("Index out of bounds!")
            return [(self.__dates[param], self.__values[param])]
        
        elif isinstance(param, slice):
            filtered_dates = self.__dates[param]
            filtered_values = self.__values[param]
            return list(zip(filtered_dates, filtered_values))
        
        elif isinstance(param, (datetime, date)):
            
            result = []
            
            for value_date, value in zip(self.__dates, self.__values):
                
                if not isinstance(value_date, (datetime, date)):
                    continue
                
                if value_date.date() == param.date():
                    result.append((value_date, value))
                elif value_date.date() > param.date():
                    break
                
            return result
        
        else:
            raise TypeError(f"Invalid parameter type: {type(param)}")
        
    @property
    def mean(self):
        return mean(self.__values) if self.__values else None

    @property
    def stddev(self):
        return stdev(self.__values) if len(self.__values) > 0 else 0.0
        