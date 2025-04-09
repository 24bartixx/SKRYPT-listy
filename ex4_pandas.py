import pandas as pd
import re
import timeit
from utils import *


def dates(df):
    
    open_dates = df[METADATA_OPEN_DATE_PL].dropna().astype(str).str.findall(DATE_PATTERN).explode().dropna().tolist()
    closure_dates = df[METADATA_CLOSURE_DATE_PL].dropna().astype(str).str.findall(DATE_PATTERN).explode().dropna().tolist()

    return open_dates + closure_dates
    

def coords(df):
    latitudes = df[METADATA_LATITUDE].dropna().astype(str).str.findall(COORDS_PATTERN).explode()
    latitudes = latitudes[latitudes != ''].dropna()

    longitudes = df[METADATA_LONGITUDE].dropna().astype(str).str.findall(COORDS_PATTERN).explode()
    longitudes = longitudes[longitudes != ''].dropna()

    return latitudes.tolist() + longitudes.tolist()


def two_compartments(df):
    return df[METADATA_STATION_NAME_PL].dropna()[
        df[METADATA_STATION_NAME_PL].dropna().str.contains(TWO_COMPARTMENTS_PATTERN)
    ].tolist()


def polish_to_latin(df):
    pattern = re.compile("|".join(POLISH_CHARS_TO_LATIN_AND_SPACE.keys()))
    return df[METADATA_STATION_NAME_PL].apply(lambda station_name: pattern.sub(
        lambda match: POLISH_CHARS_TO_LATIN_AND_SPACE[match.group(0)], 
        station_name
    )).tolist()
    
def mobile_MOB(df):
    stations = df[df[METADATA_CODE_STATION_PL].str.endswith("MOB", na = False)]
    return (stations[METADATA_STATION_TYPE_PL] == "mobilna").all()

def three_compartments(df):
    return df[df[METADATA_STATION_NAME_PL].str.contains(THREE_COMPARTMENTS_PATTERN, na = False)]
    
    
def ul_al_comma(df):
    return df[df[METADATA_ADDRESS_PL].str.contains(UL_AL_PATTERN, na = False) & df[METADATA_ADDRESS_PL].str.contains(",", na = False)]
    

def ex4():
    
    df = pd.read_csv(METADATA_FILE_PATH)
    
    print("\n===== subpoint A =====")
    print(f"Dates count: {len(dates(df))}")
    
    print("\n===== subpoint B =====")
    print(f"Coords count: {len(coords(df))}")
    
    print("\n===== subpoint C =====")
    print(f"Two compartments count: {len(two_compartments(df))}")
    
    print("\n===== subpoint D =====")
    print(f"Converted to latin alphabet: {len(polish_to_latin(df))}")
    
    print("\n===== subpoint E =====")
    print(f"MOPy mobile: {mobile_MOB(df)}")
    
    print("\n===== subpoint F =====")
    print(f"Three compartments count: {len(three_compartments(df))}")
    
    print("\n===== subpoint G =====")
    print(f"Streets or avanues with comma: {len(ul_al_comma(df))}" )



if __name__ == "__main__":    
    execution_time = timeit.timeit("ex4()", globals=globals(), number=1)
    print(f"\n\033[93mExecution time of ex4(): {execution_time} seconds\033[0m\n")
    