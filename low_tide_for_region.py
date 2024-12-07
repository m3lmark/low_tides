import itertools
import json
import requests
import sys
import time
import threading

done = False


def animate():
    """Displays a loading spinner in the console."""
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if done:
            break
        sys.stdout.write(f"\rloading {c}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\rDone!          \n")


def load_stations(file_path):
    """Loads station data from a JSON file."""
    try:
        with open(file_path) as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' is not a valid JSON file.")
        sys.exit(1)


def fetch_tide_data(station, region, start_date, end_date):
    """Fetches tide data for a specific station."""
    url = (
        f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
        f"?begin_date={start_date}&end_date={end_date}&station={station}"
        f"&product=predictions&datum=MLLW&time_zone=lst_ldt&interval=hilo"
        f"&units=english&application=DataAPI_Sample&format=json"
    )
    response = requests.get(url)
    if response.ok:
        data = response.json()
        if "error" not in data:
            return data["predictions"]
    return []


def get_lowest_tides(stations, region, start_date, end_date):
    """Fetches the lowest tides for all stations in the region."""
    station_lows = {}
    for station in stations[region]:
        predictions = fetch_tide_data(station, region, start_date, end_date)
        for prediction in predictions:
            if prediction["type"] == "L":
                tide_value = float(prediction["v"])
                if (
                    station not in station_lows
                    or tide_value < station_lows[station]["value"]
                ):
                    station_lows[station] = {
                        "time": prediction["t"],
                        "value": tide_value,
                    }
    return station_lows


def fetch_station_name(station_id):
    """Fetches the station name for a given station ID."""
    url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station_id}.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data["stations"][0]["name"]
    return "Unknown Station"


def display_results(station_lows, lowest_tide_values, region):
    """Displays the results of the lowest tides."""
    for station_id, details in station_lows.items():
        if details["value"] in lowest_tide_values:
            station_name = fetch_station_name(station_id)
            print(
                f"One of the lowest tides in {region} on {details['time'].split()[0]} "
                f"in {station_name} at {details['time'].split()[1]} "
                f"with a value of {details['value']} feet."
            )


def main():
    stations = load_stations("stations.json")

    print(
        "\nWelcome to the low tide selector. Please select a region, timeframe, "
        "and how many results you would like returned.\n"
    )
    print(
        f"Stations are available in the following regions: {', '.join(stations.keys())}\n"
    )

    region = input("Which region?\t")
    if region not in stations:
        print("Invalid region. Exiting.")
        sys.exit(1)

    start_date = input("Please enter a start date (YYYYmmdd):\t")
    end_date = input("Please enter an end date (YYYYmmdd):\t")
    num_of_results = int(input("How many results do you want?\t"))

    t = threading.Thread(target=animate, daemon=True)
    t.start()

    station_lows = get_lowest_tides(stations, region, start_date, end_date)

    global done
    done = True
    t.join()

    if not station_lows:
        print("No tide data found. Please check your input and try again.")
        return

    tide_values = sorted([details["value"] for details in station_lows.values()])
    lowest_tide_values = tide_values[:num_of_results]

    display_results(station_lows, lowest_tide_values, region)


if __name__ == "__main__":
    main()
