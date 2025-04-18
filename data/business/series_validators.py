from abc import ABC, abstractmethod
from typing import List
from ..models.time_series import TimeSeries


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
            if abs(series.values[i] - mean) <= stddev * self.k
        ]
        
    
class ThresholdDetector(SeriesValidator):
    
    def __init__(self, threshold):
        self.threshold = threshold
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        return [
            f"Measurement {series.indicator} {series.averaging_time} with value {series.values[i]} exceeded threshold {self.threshold} on {series.dates[i]}"
            for i in range(len(series.values))
            if series.values[i] > self.threshold
        ]
        
        
class ZeroSpikeDetector(SeriesValidator):
    
    def analyze(self, series: TimeSeries) -> List[str]:
        
        messages = []
        invalid = []
        
        for i in range(len(series.values)):
            if not series.values[i]:
                invalid.append(i)
            elif invalid:
                if len(invalid) >= 3:
                    msgs = []
                    for j in invalid:
                        msgs.append(f"({series.dates[j]}, {series.values[j]})")
                    messages.append("Consecutive invalid values:" + ", ".join(msgs))
                invalid = []
                
        if len(invalid) >= 3:
            msgs = []
            for i in invalid:
                msgs.append(f"({series.dates[i]}, {series.values[i]})")
            messages.append("Consecutive invalid values:" + ", ".join(msgs))
                
        return messages
        