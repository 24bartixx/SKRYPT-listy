from datetime import datetime, date
from statistics import mean, stdev
from typing import List, Union, Tuple, Optional, Sequence

class TimeSeries:
    def __init__(
        self, 
        stations_code: str,
        indicator: str,
        averaging_time: str,
        unit: str,
        dates: Sequence[Union[datetime, str]],
        values: Sequence[Union[float, str, None]]
    ) -> None:
        self.__indicator: str = indicator
        self.__station_code: str = stations_code
        self.__averaging_time: str = averaging_time
        self.__unit: str = unit
        self.__dates: List[Union[datetime, str]] = list(dates)
        self.__values: List[Union[float, str, None]] = list(values)
        
    def __str__(self) -> str:
        first_count = min(len(self.__dates), 5)
        return (
            "Station"
            f"\n\tIndicator: {self.__indicator}"
            f"\n\tStation code: {self.__station_code}"
            f"\n\tAveraging time: {self.__averaging_time}"
            f"\n\tUnit: {self.__unit}"
            f"\n\tFirst {first_count} dates: {[self.__dates[i] for i in range(first_count)]}"
            f"\n\tFirst {first_count} values: {[self.__values[i] for i in range(first_count)]}"
            f"\n\tLast {first_count} dates: {[self.__dates[i] for i in range(-first_count, 0)]}"
            f"\n\tLast {first_count} values: {[self.__values[i] for i in range(-first_count, 0)]}"
        )
        
    def __getitem__(
        self, 
        param: Union[int, slice, Union[datetime, date]]
    ) -> List[Tuple[Union[datetime, str, None], Union[float, str, None]]]:
        
        if isinstance(param, int):
            if param < -len(self.__dates) or param >= len(self.__dates):
                raise IndexError("Index out of bounds!")
            return [(self.__dates[param], self.__values[param])]
        
        elif isinstance(param, slice):
            filtered_dates = self.__dates[param]
            filtered_values = self.__values[param]
            return list(zip(filtered_dates, filtered_values))
        
        elif isinstance(param, (datetime, date)):
            
            result: List[Tuple[Union[datetime, str, None], Union[float, str, None]]] = []
            
            for value_date, value in zip(self.__dates, self.__values):
                
                if not isinstance(value_date, datetime):
                    continue
                
                if value_date.date() == (param.date() if isinstance(param, datetime) else param):
                    result.append((value_date, value))
                elif value_date.date() > (param.date() if isinstance(param, datetime) else param):
                    break
                
            if len(result) == 0:
                raise KeyError("No measurement found for the given date!")
                
            return result
        
        else:
            raise TypeError(f"Invalid parameter type: {type(param)}")
        
    @property
    def indicator(self) -> str:
        return self.__indicator
    
    @property
    def station_code(self) -> str:
        return self.__station_code
    
    @property
    def averaging_time(self) -> str:
        return self.__averaging_time
        
    @property
    def values(self) -> List[Union[float, str, None]]:
        return self.__values
        
    @property
    def dates(self) -> List[Union[datetime, str]]:
        return self.__dates
        
    @property
    def mean(self) -> Optional[float]:
        values = [value for value in self.__values if isinstance(value, (float, int))]
        return mean(values) if values else None

    @property
    def stddev(self) -> float:
        values = [value for value in self.__values if isinstance(value, (float, int))]
        return stdev(values) if len(values) > 0 else 0.0
        
        
    