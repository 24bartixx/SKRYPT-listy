from pathlib import Path
import re
from utils import logger, MEASUREMENTS_CATALOG, KEY_TUPLE_PATTERN


log = logger()


def group_measurement_files_by_key(catalog_path = MEASUREMENTS_CATALOG):
    
    pattern = re.compile(KEY_TUPLE_PATTERN)
    
    files_dict = {}
    
    if catalog_path.exists() and catalog_path.is_dir():
        for csv_file in filter(lambda path: path.is_file and path.suffix == ".csv", catalog_path.iterdir()):
            
            match = pattern.search(csv_file.name)
            
            if match:
                key_tuple = int(match.group(1)), match.group(2), match.group(3)
                files_dict[key_tuple] = csv_file
            
        return files_dict
                    
    else:
        log.error(f"The path {catalog_path} is not a catalog!")
        raise FileNotFoundError(f"{catalog_path} not found or not directory.")


def main():
    measurements = group_measurement_files_by_key()
    log.info(f"Dictonary created with {len(measurements.keys())} keys!")
    
    print("\nMeasurements:")
    for key, measurement in measurements.items():
        print(f"\t{key} => {measurement}")


if __name__ == "__main__":
   main()
    