import pytest 
from datetime import datetime
from pathlib import Path
from classes.measurements import Measurements
from classes.time_series import TimeSeries
from classes.series_validators import *

values = [0.24, 0.1512, 0.934, 0.4, None, 1325.42411, 0.6029, 0.15]
    
time_series = TimeSeries(
    stations_code="station_code",
    indicator="indicator",
    averaging_time="averaging_time",
    unit="unit",
    dates=[datetime(2025, 5, i) for i in range(1,len(values)+1)],
    values=values
)

measurements = Measurements(Path("data/measurements/"))
measurements.get_by_station("LuNowaSolKos")

analyzers1 = [OutlierDetector(2), ZeroSpikeDetector(), SimpleValidator()]
analyzers2 = [OutlierDetector(3), SimpleValidator(), ZeroSpikeDetector(), ThresholdDetector(0.6)]
analyzers3 = [
    SimpleValidator(),
    CompositeValidator(
        validators=[ThresholdDetector(0.7), OutlierDetector(1.5)], 
        mode = CompositeValidator.MODE.OR
    ),
    CompositeValidator(
        validators=[ThresholdDetector(0.4), OutlierDetector(0.7)], 
        mode = CompositeValidator.MODE.AND
    )
]

@pytest.mark.parametrize("validators", [analyzers1])
def test_detect_all_anomalies(validators):
    result = measurements.detect_all_anomalies(validators)
    
    assert len(result) >= 0
    
    try:
        [msg for msg in result]
    except TypeError:
        pytest.fail("Result is not iterable")
    
    try:
        " ".join(result)
    except Exception:
        pytest.fail("Cannot concatenate anomalies' messages")
    
    
    