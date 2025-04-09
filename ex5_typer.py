import typer
from datetime import datetime, date
from ex5 import *


app = typer.Typer()
        
def valid_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise typer.BadParameter("Expected date fromat: yyyy-mm-dd")


@app.command(COMMAND_RANDOM)
def random_command(
    measurement: str = typer.Argument(..., help = "The type of measured value (e.g. PM10, PM2.5, NO)"),
    frequency: str = typer.Argument(..., help = "Frequency of measurements (e.g. 1g, 24g)"),
    start_date = typer.Argument(..., callback = valid_date, help = "Start date of the measurement (format: yyyy-mm-dd)"),
    end_date = typer.Argument(..., callback = valid_date, help = "End date of the measurement (format: yyyy-mm-dd)")
):

    result = random_station_name(measurement, frequency, start_date, end_date)
    print("\n\tResult: ", result, "\n")
    
    
@app.command(COMMAND_STATION)
def station_command(
    measurement: str = typer.Argument(..., help = "The type of measured value (e.g. PM10, PM2.5, NO)"),
    frequency: str = typer.Argument(..., help = "Frequency of measurements (e.g. 1g, 24g)"),
    start_date = typer.Argument(..., callback = valid_date, help = "Start date of the measurement (format: yyyy-mm-dd)"),
    end_date = typer.Argument(..., callback = valid_date, help = "End date of the measurement (format: yyyy-mm-dd)"),
    station_name: str = typer.Option(..., help = "Name of the station"),
):
    
    mean, stddev, decimal_places = mean_and_standard_variation(
        measurement, frequency, start_date, end_date, station_name
    )
    
    print(f"\n\tMean: {round(mean, decimal_places)}")
    print(f"\tStandard deviation: {round(stddev, decimal_places)}\n")
    
@app.command(COMMAND_ANOMALIES)
def station_command(
    measurement: str = typer.Argument(..., help = "The type of measured value (e.g. PM10, PM2.5, NO)"),
    frequency: str = typer.Argument(..., help = "Frequency of measurements (e.g. 1g, 24g)"),
    start_date = typer.Argument(..., callback = valid_date, help = "Start date of the measurement (format: yyyy-mm-dd)"),
    end_date = typer.Argument(..., callback = valid_date, help = "End date of the measurement (format: yyyy-mm-dd)"),
    station_name: str = typer.Option(..., help = "Name of the station"),
):
    
    result = anomalies(
        measurement, frequency, start_date, end_date, station_name
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
    app()
    