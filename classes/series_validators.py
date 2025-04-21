from abc import ABC, abstractmethod
from typing import List
from classes.time_series import TimeSeries
from datetime import datetime
from enum import Enum
from collections import deque
import re
import heapq


class SeriesValidator(ABC):
    
    @abstractmethod
    def analyze(series: TimeSeries) -> List[str]:
        pass
    
    
class OutlierDetector(SeriesValidator):
    
    def __init__(self, k):
        self.k = k
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        mean = series.mean
        stddev = series.stddev
        
        return [
            f"Measurement {series.indicator} {series.averaging_time} with value {series.values[i]} on {series.dates[i]} exceeded standard deviation" 
            for i in range(len(series.values)) 
            if isinstance(series.values[i], float) and abs(series.values[i] - mean) > stddev * self.k
        ]
        
    
class ThresholdDetector(SeriesValidator):
    
    def __init__(self, threshold):
        self.threshold = threshold
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        return [
            f"Measurement {series.indicator} {series.averaging_time} with value {series.values[i]} exceeded threshold {self.threshold} on {series.dates[i]}"
            for i in range(len(series.values))
            if isinstance(series.values[i], float) and series.values[i] > self.threshold
        ]
        
        
class ZeroSpikeDetector(SeriesValidator):
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        messages = []
        invalid = []
        
        for i in range(len(series.values)):
            if not series.values[i] or not isinstance(series.values[i], float):
                invalid.append(i)
            elif invalid:
                if len(invalid) >= 3:
                    msgs = []
                    for j in invalid:
                        msgs.append(f"({series.dates[j]}, {series.values[j]})")
                    messages.append("Consecutive invalid values: " + ", ".join(msgs))
                invalid = []
                
        if len(invalid) >= 3:
            msgs = []
            for i in invalid:
                msgs.append(f"({series.dates[i]}, {series.values[i]})")
            messages.append("Consecutive invalid values:"  + ", ".join(msgs))
                
        return messages
    
    
# extended version
class CompositeValidator(SeriesValidator):
    
    DATE_PATTERN = r"^.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*$"
    
    class MODE(Enum):
        OR = "or"
        AND = "and"
    
    def __init__(self, validators, mode):
        if not isinstance(mode, CompositeValidator.MODE):
            raise ValueError(f"Mode must be an instance of CompositeValidator.MODE, got {mode}")
        self.validators = validators
        self.mode = mode
        
    
    
    def __get_list_to_sort(self, series):
        
        pattern = re.compile(CompositeValidator.DATE_PATTERN)
        lists_to_sort = []
        
        for list_index in range(len(self.validators)):
            
            messages = self.validators[list_index].analyze(series)
            lists_to_sort.append(deque())
            
            for message in messages:
                dates = pattern.findall(message)
                if dates:
                    latest = min(datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates)
                    lists_to_sort[-1].append((latest, message, list_index))
                    
        return lists_to_sort
    
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        lists_to_sort = self.__get_list_to_sort(series)
        
        if self.mode == CompositeValidator.MODE.OR:
            
            heap = []
            result = []
            
            for message_items in lists_to_sort:
                heapq.heappush(heap, message_items.popleft())
                    
            while heap:
                date, message, list_index = heapq.heappop(heap)
                
                if len(lists_to_sort[list_index]) > 0:
                    heapq.heappush(heap, lists_to_sort[list_index].popleft())
                
                result.append((date, message))
                
            return [item[1] for item in result]
                
                    
        elif self.mode == CompositeValidator.MODE.AND:
        
            heap = []
            result = []
            temp_messages = set()
            temp_date = None
            
            for message_items in lists_to_sort:
                heapq.heappush(heap, message_items.popleft())
                    
            while heap:
                date, message, list_index = heapq.heappop(heap)
                
                if len(lists_to_sort[list_index]) > 0:
                    heapq.heappush(heap, lists_to_sort[list_index].popleft())
                
                if not temp_date or temp_date != date:
                    temp_messages = {message}
                    temp_date = date
                else:
                    temp_messages.add(message)
                    
                if len(temp_messages) == len(self.validators):
                    result += list(temp_messages)
                    temp_messages = set()
                    temp_date = None
                        
            return result
        
        raise ValueError(f"Unsupported mode: {self.mode}")
                
        
class SimpleValidator:
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        return [f"Info: {series.indicator} {series.averaging_time} at {series.station_code} has mean = {series.mean}"]
        