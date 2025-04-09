import argparse
from ex5 import *
            
def parse_arguments():
    
    def valid_date(date):
        try:
            return datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise argparse.ArgumentTypeError("Expected date fromat: yyyy-mm-dd")
    
    parser = argparse.ArgumentParser()
    
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("measurement", help = "The type of measured value (e.g. PM10, PM2.5, NO)")
    parent_parser.add_argument("frequency", help="Frequency of measurements (e.g. 1g, 24g)")
    parent_parser.add_argument("start", type = valid_date, help = "Start date of the measurement (format: yyyy-mm-dd)")
    parent_parser.add_argument("end", type = valid_date, help = "End date of the measurement (format: yyyy-mm-d)")
    
    subparsers = parser.add_subparsers(dest = "command", required = True)
    
    subparsers.add_parser(COMMAND_RANDOM, parents=[parent_parser], help = "Random station result option")
    
    argument_parser = subparsers.add_parser(COMMAND_STATION, parents=[parent_parser], help = "Chosen station result option")
    argument_parser.add_argument("--station_name", required = True, help = "Name of the station")
    
    anomalies_parser = subparsers.add_parser(COMMAND_ANOMALIES, parents=[parent_parser], help="Anomalies detection option")
    anomalies_parser.add_argument("--station_name", required=True, help="Name of the station")
    
    return parser.parse_args()


def ex5():
    args = parse_arguments()
    
    if args.command == COMMAND_RANDOM:
        
        result = random_station_name(args.measurement, args.frequency, args.start, args.end)
        print("\n\tResult: ", result, "\n")
        
    elif args.command == COMMAND_STATION:
        
        mean, stddev, decimal_places = mean_and_standard_variation(args.measurement, args.frequency, args.start, args.end, args.station_name)
        print(f"\n\tMean: {round(mean, decimal_places)}")
        print(f"\tStandard deviation: {round(stddev, decimal_places)}\n")

    elif args.command == COMMAND_ANOMALIES:
        
        result = anomalies(
            args.measurement, args.frequency, args.start, args.end, args.station_name
        )
        
        for year, stats in result.items():
            print(f"\n===== {year} =====")
            print("\tDiffs:")
            for change in stats[ANOMALIES_CHANGE]:
                print(f"\t\t{change}")
            print("\tIncorrect:")
            for incorrect in stats[ANOMALIES_INCORRECT]:
                print(f"\t\t{incorrect}")
            print("\tToo high:")
            for too_high in stats[ANOMALIES_TOO_HIGH]:
                print(f"\t\t{too_high}")
        print()


if __name__ == "__main__":
    ex5()
