import pytest
from datetime import datetime, date
from classes.time_series import TimeSeries

values = [0.02 + 0.03*i for i in range(31)]

time_series: TimeSeries = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[datetime(2025, 5, i) for i in range(1, 32)],
    values=values
)

# ===== ex 4b-i =====
def test_index():
    result = time_series[3]
    assert isinstance(result, list)
    pair = result[0]
    assert isinstance(pair, tuple)
    date = pair[0]
    assert isinstance(date, datetime)
    value = pair[1]
    assert isinstance(value, float)
    assert value == 0.11
    assert time_series[25][0][1] == 0.77

# ===== ex 4b-ii =====
def test_slice():
    my_slice = slice(3,8,2)
    sliced = time_series[my_slice]
    assert len(sliced) == 3
    assert sliced[0][0] == datetime(2025,5,4)
    assert sliced[0][1] == 0.11
    assert sliced[1][0] == datetime(2025,5,6)
    assert sliced[1][1] == pytest.approx(0.17)
    assert sliced[2][0] == datetime(2025,5,8)
    assert sliced[2][1] == pytest.approx(0.23)
    
# ===== ex 4b-iii =====
def test_datetime():
    result = time_series[date(2025,5,24)]
    assert isinstance(result, list)
    pair = result[0]
    assert isinstance(pair, tuple)
    result_date = pair[0]
    value = pair[1]
    assert isinstance(result_date, datetime)
    assert isinstance(value, float)
    assert result_date == datetime(2025,5,24)
    assert value == 0.71  
    
# ===== ex 4b-iv =====
def test_invalid_datetime():
    with pytest.raises(KeyError):
        time_series[date(2025,6,24)]
        
# ===== ex 4c-i =====
def test_mean():
    mean = sum(values) / len(values)
    assert time_series.mean == pytest.approx(mean)
    
# ===== ex 4c-ii =====
def test_stddev():
    from statistics import stdev
    assert time_series.stddev == stdev(values)
    