from pathlib import Path
from utils import logger, MEASUREMENTS_CATALOG


log = logger()


def group_measurement_files_by_key(catalog_path = MEASUREMENTS_CATALOG):
    
    files_dict = {}
    
    if catalog_path.exists() and catalog_path.is_dir():
        for csv_file in filter(lambda path: path.is_file and path.suffix == ".csv", catalog_path.iterdir()):
            name_list = csv_file.name.removesuffix(".csv").split("_")
            name_tuple = int(name_list[0]), name_list[1], name_list[2]
            
            files_dict[name_tuple] = csv_file
            
        return files_dict
                    
    else:
        log.error(f"The path {catalog_path} is not a catalog!")
        raise FileNotFoundError(f"{catalog_path} not found or not directory.")


def main():
    measurements = group_measurement_files_by_key()
    log.info(f"Dictonary created with {len(measurements.keys())} keys!")


if __name__ == "__main__":
   main()
    