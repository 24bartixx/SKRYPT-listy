import pytest
from classes.station import Station

# ===== ex 4a =====

def test_station_not_equal_to_different_type():
    station = Station(1, "ABC123", "OC1", "2023-01-01", "2024-01-01")
    assert station != 44

@pytest.mark.parametrize(
    "args1, args2",
    [
        # same code, same parameters
        (
            (1, "ABC123", "OC1", "2023-01-01", "2024-01-01"),
            (1, "ABC123", "OC1", "2023-01-01", "2024-01-01")  
        ),
        # same code, different parameters
        (
            (1, "XYZ789", "OC1", "2023-01-01", "2024-01-01"),
            (2, "XYZ789", "OC2", "2023-06-01", "2025-01-01")
        )
    ]
)
def test_station_eq(args1, args2):
    station1 = Station(*args1)
    station2 = Station(*args2)
    assert station1 == station2
    
    
@pytest.mark.parametrize(
    "args1, args2",
    [
        # different code, same parameters
        (
            (1, "NJD910", "OC1", "2023-01-01", "2024-01-01"),
            (1, "NJD837", "OC1", "2023-01-01", "2024-01-01")  
        ),
        # different code, different parameters
        (
            (1, "AAA111", "OC1", "2023-01-01", "2024-01-01"),
            (2, "BBB222", "OC2", "2023-06-01", "2025-01-01")
        ),
        # different code, different parameters
        (
            (3, "XYZ123", "OC3", "2022-05-05", "2023-05-05"),
            (4, "LMN456", "OC4", "2021-01-01", "2022-01-01")
        )
    ]
)
def test_station_not_eq(args1, args2):
    station1 = Station(*args1)
    station2 = Station(*args2)
    assert station1 != station2
