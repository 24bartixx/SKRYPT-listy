import pandas as pd
import re
import timeit
from utils import *
from read_data import read_metadata


def dates(stations):
    return [
        date
        for station in stations
        for date in (station[METADATA_OPEN_DATE_PL], station[METADATA_CLOSURE_DATE_PL])
        if re.search(DATE_PATTERN, date)
    ]
    
def coords(stations):
    
    return [
        coord
        for station in stations
        for coord in (station[METADATA_LATITUDE], station[METADATA_LONGITUDE])
        if re.search(COORDS_PATTERN, coord)
    ]

def two_compartments(stations):
    return [
        station[METADATA_STATION_NAME_PL]
        for station in stations
        if re.search(TWO_COMPARTMENTS_PATTERN, station[METADATA_STATION_NAME_PL])
    ]

def polish_to_latin(stations):
    
    pattern = re.compile("|".join(POLISH_CHARS_TO_LATIN_AND_SPACE.keys()))
    
    return [
        pattern.sub(lambda m: POLISH_CHARS_TO_LATIN_AND_SPACE[m.group(0)], station[METADATA_STATION_NAME_PL])
        for station in stations
    ]
    
def mobile_MOB(stations):
    
    for station in stations:
        if re.search(MOB_PATTERN, station[METADATA_CODE_STATION_PL])and not re.search(MOBILE_PATTERN, station[METADATA_STATION_TYPE_PL]):
            return False
    
    return True

def three_compartments(stations):
    return [
        station
        for station in stations
        if re.search(THREE_COMPARTMENTS_PATTERN, station[METADATA_STATION_NAME_PL])
    ]
    
def ul_al_comma(stations):
    return [
        station
        for station in stations
        if re.search(UL_AL_PATTERN, station[METADATA_ADDRESS_PL])
    ]

def ex4():

    stations = read_metadata(METADATA_FILE_PATH)[METADATA_STATIONS]
    
    print("\n===== subpoint A =====")
    print(f"Dates count: {len(dates(stations))}")
    
    print("\n===== subpoint B =====")
    print(f"Coords count: {len(coords(stations))}")
    
    print("\n===== subpoint C =====")
    print(f"Two compartments count: {len(two_compartments(stations))}")
    
    print("\n===== subpoint D =====")
    print(f"Converted to latin alphabet: {len(polish_to_latin(stations))}")
    
    print("\n===== subpoint E =====")
    print(f"MOBy mobile: {mobile_MOB(stations)}")
    
    print("\n===== subpoint F =====")
    print(f"Three compartments count: {len(three_compartments(stations))}")
    
    print("\n===== subpoint G =====")
    print(f"Streets or avanues with comma: {len(ul_al_comma(stations))}" )



if __name__ == "__main__":    
    execution_time = timeit.timeit("ex4()", globals=globals(), number=1)
    print(f"\n\033[93mExecution time of ex4(): {execution_time} seconds\033[0m\n")
    