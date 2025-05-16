from abc import ABC, abstractmethod
from typing import List, Optional,Deque, Tuple, Set, Union
from classes.time_series import TimeSeries
from datetime import datetime
from enum import Enum
from collections import deque
import re
import heapq


ValidatorMessage = Tuple[datetime, str, int]


class SeriesValidator(ABC):
    
    @abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        pass
    
    
class OutlierDetector(SeriesValidator):
    
    def __init__(self, k: float) -> None:
        self.k : float = k
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        if len(series.values) == 0:
            return []
        
        mean : Optional[float] = series.mean
        stddev : float = series.stddev
          
        return [
            f"Measurement {series.indicator} {series.averaging_time} with value {series.values[i]} on {series.dates[i]} exceeded standard deviation" 
            for i in range(len(series.values)) 
            if isinstance(value := series.values[i], Union[float, int]) and abs(value - mean) > stddev * self.k
        ]
        
    
class ThresholdDetector(SeriesValidator):
    
    def __init__(self, threshold: float) -> None:
        self.threshold : float = threshold
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        return [
            f"Measurement {series.indicator} {series.averaging_time} with value {series.values[i]} exceeded threshold {self.threshold} on {series.dates[i]}"
            for i in range(len(series.values))
            if isinstance(value := series.values[i], Union[float, int]) and value > self.threshold
        ]
        
        
class ZeroSpikeDetector(SeriesValidator):
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        messages: List[str] = []
        invalid: List[int]  = []
        
        for i in range(len(series.values)):
            if not series.values[i] or not isinstance(series.values[i], Union[float, int]):
                invalid.append(i)
            elif invalid:
                if len(invalid) >= 3:
                    invalid_msgs: List[str] = []
                    for j in invalid:
                        invalid_msgs.append(f"({series.dates[j]}, {series.values[j]})")
                    messages.append("Consecutive invalid values: " + ", ".join(invalid_msgs))
                invalid = []
                
        if len(invalid) >= 3:
            leftover_msgs: List[str] = []
            for i in invalid:
                leftover_msgs.append(f"({series.dates[i]}, {series.values[i]})")
            messages.append("Consecutive invalid values: "  + ", ".join(leftover_msgs))
                
        return messages
    
    
# extended version
class CompositeValidator(SeriesValidator):
    
    DATE_PATTERN: str = r"^.*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*$"
    
    class MODE(Enum):
        OR = "or"
        AND = "and"
    
    def __init__(self, validators: List[SeriesValidator], mode: MODE) -> None:
        # if not isinstance(mode, CompositeValidator.MODE):
        #     raise ValueError(f"Mode must be an instance of CompositeValidator.MODE, got {mode}")
        self.validators: List[SeriesValidator] = validators
        self.mode: CompositeValidator.MODE = mode
        
    
    def __get_list_to_sort(self, series: TimeSeries) -> List[Deque[ValidatorMessage]]:
        
        pattern: re.Pattern[str] = re.compile(CompositeValidator.DATE_PATTERN)
        lists_to_sort: List[Deque[ValidatorMessage]] = []
        
        for list_index in range(len(self.validators)):
            
            messages: List[str] = self.validators[list_index].analyze(series)
            lists_to_sort.append(deque())
            
            for message in messages:
                dates: List[str] = pattern.findall(message)
                if dates:
                    latest: datetime = min(datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates)
                    lists_to_sort[-1].append((latest, message, list_index))
                    
        return lists_to_sort
    
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        lists_to_sort: List[Deque[ValidatorMessage]] = self.__get_list_to_sort(series)
        
        if self.mode == CompositeValidator.MODE.OR:
            
            heap_or: List[ValidatorMessage] = []
            result_or: List[str]  = []
            
            for message_items in lists_to_sort:
                heapq.heappush(heap_or, message_items.popleft())
                    
            while heap_or:
                _, message, list_index = heapq.heappop(heap_or)
                
                if len(lists_to_sort[list_index]) > 0:
                    heapq.heappush(heap_or, lists_to_sort[list_index].popleft())
                
                result_or.append(message)
                
            return [item for item in result_or]
                
                    
        elif self.mode == CompositeValidator.MODE.AND:
        
            heap_and: List[ValidatorMessage] = []
            result_and: List[str]  = []
            temp_messages: Set[str] = set()
            temp_date: Optional[datetime] = None
            
            for message_items in lists_to_sort:
                heapq.heappush(heap_and, message_items.popleft())
                    
            while heap_and:
                date, message, list_index = heapq.heappop(heap_and)
                
                if len(lists_to_sort[list_index]) > 0:
                    heapq.heappush(heap_and, lists_to_sort[list_index].popleft())
                
                if not temp_date or temp_date != date:
                    temp_messages = {message}
                    temp_date = date
                else:
                    temp_messages.add(message)
                    
                if len(temp_messages) == len(self.validators):
                    result_and += list(temp_messages)
                    temp_messages = set()
                    temp_date = None
                        
            return result_and
        
        raise ValueError(f"Unsupported mode: {self.mode}")
                
        
class SimpleValidator:
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        return [f"Info: {series.indicator} {series.averaging_time} at {series.station_code} has mean = {series.mean}"]
        