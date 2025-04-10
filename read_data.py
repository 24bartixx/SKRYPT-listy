import csv
import json
from pathlib import Path
from datetime import datetime
from utils import *


log = logger()


def read_metadata(file_path, should_save = False, should_log = False) -> dict:
    
    metadata = {}
    
    if file_path.exists() and file_path.is_file() and file_path.suffix == ".csv":
        try:
            with open(file_path, "r", encoding = "utf-8") as file:
                
                if should_log:
                    log.info(f"Metadata csv {file_path} file opened!")
                
                reader  = csv.reader(file)
                
                # ===== WITHOUT LOGGING XD =====
                # headers = [header.replace("\n","") for header in next(reader)]
                # metadata[METADATA_STATIONS] = [(dict(zip(headers, row))) for row in reader]
                
                headers = next(reader)
                if should_log:
                    log.debug(f"Read line: {len(",".join(headers))} bytes")
                headers = [header.replace("\n","") for header in headers]
                
                metadata[METADATA_STATIONS] = []
                for row in reader:
                
                    if should_log:
                        log.debug(f"Read line: {len(",".join(row))} bytes")
                    
                    metadata[METADATA_STATIONS].append(dict(zip(headers, row)))
                
        except:
                log.error(f"An error occured while reading file {file_path}")
                raise
            
        finally:
            if should_log:
                log.info(f"Metadata csv {file_path} file closed!")
            
        if should_save:
            save_to_json(metadata, METADATA_RESULT_PATH)
                
        return metadata
    
    else:
        log.error(f"Metadata data file {file_path} doesn't exist or is not a CSV!")
        raise FileNotFoundError(f"{file_path} not found or invalid format.")
    
    
def read_measurements(catalog_path, should_save = False, should_log = False, filter_key = "") -> list:
    
    if catalog_path.exists() and catalog_path.is_dir():
        
        data = {}
        data_list = data[MEASUREMENTS_MEASUREMENTS] = {}
        
        for csv_file in filter(
            lambda path: path.is_file() and path.suffix == ".csv" and filter_key in path.name, 
            catalog_path.iterdir()
        ):
            
            log.info(f"Reading file {csv_file}!")
            
            key = csv_file.name
            data_list[key] = []
            
            try:
                with open(csv_file, "r", encoding="utf-8") as file:
                    
                    if should_log:
                        log.info(f"Measurements csv {csv_file} file opened!")
            
                    reader = csv.reader(file)
                    to_omit = next(reader)
                    if should_log:
                        log.debug(f"Read line: {len(",".join(to_omit))} bytes")
                    
                    stations_codes = next(reader)
                    indicators = next(reader)
                    averagingTimes = next(reader)
                    units = next(reader)
                    position_codes = next(reader)
                    
                    if should_log:
                        log.debug(f"Read line: {len(",".join(stations_codes))} bytes")
                        log.debug(f"Read line: {len(",".join(indicators))} bytes")
                        log.debug(f"Read line: {len(",".join(averagingTimes))} bytes")
                        log.debug(f"Read line: {len(",".join(units))} bytes")
                        log.debug(f"Read line: {len(",".join(position_codes))} bytes")
                    
                    for station_code, indicator, averagingTime, unit, position_code in zip(
                        stations_codes[1:],
                        indicators[1:],
                        averagingTimes[1:],
                        units[1:],
                        position_codes[1:],
                    ):
                        data_list[key].append({
                            MEASUREMENTS_STATION_CODE: station_code,
                            MEASUREMENTS_INDICATOR: indicator,
                            MESAUREMENTS_AVERAGING_TIME: averagingTime,
                            MEASUREMENTS_UNIT: unit,
                            MEASUREMENTS_POSITION_CODE: position_code,
                            MEASUREMENTS_MEASUREMENTS: []
                        })
                        
                    
                    for measurements in reader:
                        
                        if should_log:
                            log.debug(f"Read line: {len(",".join(measurements))} bytes")
                        
                        try:
                            time = datetime.strptime(measurements[0], "%m/%d/%y %H:%M")
                        except ValueError:
                            for i in range(len(measurements)-1):
                                data_list[key][i][MEASUREMENTS_YEAR] = measurements[i+1]
                        else:
                            for i in range(len(measurements)-1):
                                try:
                                    data_list[key][i][MEASUREMENTS_MEASUREMENTS].append({
                                        MEASUREMENTS_TIME: time, 
                                        MEASUREMENTS_VALUE: float(measurements[i+1])
                                    })
                                except ValueError:
                                    data_list[key][i][MEASUREMENTS_MEASUREMENTS].append({
                                        MEASUREMENTS_TIME: time, 
                                        MEASUREMENTS_VALUE: None
                                    })
                                    
                    log.info(f"File {csv_file} read!")
            
            except:
                log.error(f"An error occured while reading file {csv_file}")
                raise
            
            finally:
                if should_log:
                    log.info(f"Measurements csv {csv_file} file opened!")
                
        if should_save:
            save_to_json(data, MEASUREMENTS_RESULT_PATH)
        
        return data
        
    else:
        log.error(f"The path {catalog_path} is not a catalog!")
        raise FileNotFoundError(f"{catalog_path} not found or not directory.")


def read_data(metadata_path = METADATA_FILE_PATH, measurements_catalog_path = MEASUREMENTS_CATALOG, should_save = False) -> dict:
    
    data =  {}
    
    data |= read_metadata(metadata_path, should_save = should_save)
    data |= read_measurements(measurements_catalog_path, should_save)
    
    if should_save:
        save_to_json(data, DATA_RESULT_PATH)
    
    return data


def save_to_json(data, file_path):
    
    def serialize(element):
        if isinstance(element, datetime):
            return element.strftime("%Y-%m-%d %H:%M")
        return element
          
    try:
        log.info(f"Saving json {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default = serialize)
        log.info(f"Json {file_path} saved!")
    except Exception as e:
        log.error(f"Failed to save json {file_path}: {e}")


if __name__  == "__main__":
    read_data(should_save = True)
    
    