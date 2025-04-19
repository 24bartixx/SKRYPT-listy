from pathlib import Path
from classes.measurements import Measurements
from classes.series_validators import *


def print_anomalies(anomalies):
    print("\nAnomalies")
    for key, values in anomalies.items():
        print(f"\t{key}: {len(values)}")
        i = 0
        while i < len(values) and i < 3:
            print("\t\t", values[i])
            i += 1


def measurements_tests():
    measurements = Measurements(Path("data/measurements/"))
    
    # __len__
    print(f"\nLength: {len(measurements)}")
    
    # __contains__
    print(f"\nContains NO2: {"NO2" in measurements}")
    print(f"Contains Jony_PM25: {"Jony_PM25" in measurements}")
    print(f"Contains NH4+(PM2.5): {"NH4+(PM2.5)" in measurements}")
    print(f"Contains BbF(PM10): {"BbF(PM10)" in measurements}")
    print(f"Contains PrekursoryZielonka: {"PrekursoryZielonka" in measurements}")
    print(f"Contains 123trimetylobenzen: {"123trimetylobenzen" in measurements}")
    print(f"Contains NO3: {"NO3" in measurements}")
    print(f"Contains NonExistantElement: {"NonExistantElement" in measurements}")
    
    # get_by_paremeter
    param_CO = measurements.get_by_parameter("CO")
    print(f"\nGet by parameter CO: {len(param_CO)}")
    
    param_formaldehyd = measurements.get_by_parameter("formaldehyd")
    print(f"Get by parameter formaldehyd: {len(param_formaldehyd)}")
    print(f"formaldehyd values count: {len(param_formaldehyd[0].values)}")
    
    param_NO2 = measurements.get_by_parameter("NO2")
    print(f"Get by parameter NO2: {len(param_NO2)}")
    
    param_K_PM2_5 = measurements.get_by_parameter("K+(PM2.5)")
    print(f"Get by parameter K+(PM2.5): {len(param_K_PM2_5)}")
    
    param_CO = measurements.get_by_parameter("CO")
    print(f"Get by parameter CO: {len(param_CO)}")
    
    param_formaldehyd = measurements.get_by_parameter("formaldehyd")
    print(f"Get by parameter formaldehyd: {len(param_formaldehyd)}")
    print(f"formaldehyd values count: {len(param_formaldehyd[0].values)}")
    
    param_NO2 = measurements.get_by_parameter("NO2")
    print(f"Get by parameter NO2: {len(param_NO2)}")
    
    param_K_PM2_5 = measurements.get_by_parameter("K+(PM2.5)")
    print(f"Get by parameter K+(PM2.5): {len(param_K_PM2_5)}")
    
    # get_by_station
    station_DsJelGorOgin = measurements.get_by_station("DsJelGorOgin")
    print(f"\nGet by station DsJelGorOgin: {len(station_DsJelGorOgin)}")
    
    station_KpZielBoryTu = measurements.get_by_station("KpZielBoryTu")
    print(f"Get by station KpZielBoryTu: {len(station_KpZielBoryTu)}")
    
    station_LuNowaSolKos = measurements.get_by_station("LuNowaSolKos")
    print(f"Get by station LuNowaSolKos: {len(station_LuNowaSolKos)}")
    
    station_DsJelGorOgin = measurements.get_by_station("DsJelGorOgin")
    print(f"Get by station DsJelGorOgin: {len(station_DsJelGorOgin)}")
    
    station_KpZielBoryTu = measurements.get_by_station("KpZielBoryTu")
    print(f"Get by station KpZielBoryTu: {len(station_KpZielBoryTu)}")
    
    station_LuNowaSolKos = measurements.get_by_station("LuNowaSolKos")
    print(f"Get by station LuNowaSolKos: {len(station_LuNowaSolKos)}")
    
    validators = [
        OutlierDetector(4),
        # ThresholdDetector(0),
        # ZeroSpikeDetector(),
        SimpleValidator()
    ]
    
    measurements = Measurements(Path("data/measurements/"))
    measurements.get_by_station("LuNowaSolKos")
    
    anomalies = measurements.detect_all_anomalies(validators)
    print_anomalies(anomalies)
        
    anomalies = measurements.detect_all_anomalies(validators)
    print_anomalies(anomalies)
            
    anomalies = measurements.detect_all_anomalies(validators, preload=True)
    print_anomalies(anomalies)
    
    
if __name__ == "__main__":
    measurements_tests()
    