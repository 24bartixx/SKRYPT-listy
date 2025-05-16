from datetime import datetime
from classes.series_validators import ZeroSpikeDetector
from classes.time_series import TimeSeries

values = [0.342, 0.1345, 1.34, None, 0, None, None, 0, 1, 0, 0, 0, 0.15, 0.196, None, None, None, 0.51]
    
time_series = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[datetime(2025, 5, i) for i in range(1,len(values)+1)],
    values=values
)

def test_zero_spike_detector():
    result = ZeroSpikeDetector().analyze(time_series)
    
    assert isinstance(result, list)
    assert len(result) == 3
    assert "Consecutive invalid values: (2025-05-04 00:00:00, None), (2025-05-05 00:00:00, 0), (2025-05-06 00:00:00, None), (2025-05-07 00:00:00, None), (2025-05-08 00:00:00, 0)"
    assert "Consecutive invalid values: (2025-05-10 00:00:00, 0), (2025-05-11 00:00:00, 0), (2025-05-12 00:00:00, 0)"
    assert "Consecutive invalid values: (2025-05-15 00:00:00, None), (2025-05-16 00:00:00, None), (2025-05-17 00:00:00, None)"