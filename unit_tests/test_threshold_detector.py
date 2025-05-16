from datetime import datetime
from classes.series_validators import ThresholdDetector
from classes.time_series import TimeSeries

values = [10, 532.23, 15.513, 0.314, 5, 7.4, 100.5, -14.25]
    
time_series = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[datetime(2025, 5, i) for i in range(1,len(values)+1)],
    values=values
)

empty_time_series = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[],
    values=[]
)

def test_zero_spike_detector():
    detector = ThresholdDetector(9)
    result = detector.analyze(time_series)
    empty_result = detector.analyze(empty_time_series)
    
    assert isinstance(result, list)
    assert len(result) == 4
    assert "Measurement indicator averaging_time with value 10 exceeded threshold 9 on 2025-05-01 00:00:00" in result
    assert "Measurement indicator averaging_time with value 532.23 exceeded threshold 9 on 2025-05-02 00:00:00" in result
    assert "Measurement indicator averaging_time with value 15.513 exceeded threshold 9 on 2025-05-03 00:00:00" in result
    assert "Measurement indicator averaging_time with value 100.5 exceeded threshold 9 on 2025-05-07 00:00:00" in result
    
    assert isinstance(empty_result, list)
    assert len(empty_result) == 0
    