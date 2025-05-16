from datetime import datetime
from classes.time_series import TimeSeries
from classes.series_validators import OutlierDetector
    
values = [-592, 10.05, 12.11, 23.4321, 23.1, 16, 23.4013, 21.120342, 16.7, 0.3, 100.21, 610.32, 245, 1204.6]
    
time_series = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[datetime(2025, 5, i) for i in range(1,len(values)+1)],
    values=values
)

def test_outlier_detector():
    result = OutlierDetector(1.2).analyze(time_series)

    assert isinstance(result, list)
    assert len(result) == 3
    assert "Measurement indicator averaging_time with value 1204.6 on 2025-05-14 00:00:00 exceeded standard deviation" in result
    assert "Measurement indicator averaging_time with value -592 on 2025-05-01 00:00:00 exceeded standard deviation" in result
    assert "Measurement indicator averaging_time with value 610.32 on 2025-05-12 00:00:00 exceeded standard deviation" in result
    
    
    
    