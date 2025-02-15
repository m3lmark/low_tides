from flask import render_template, request
from app import app
import json
import requests
from datetime import datetime
import concurrent.futures
import folium


def load_stations(filename):
    """Loads station data from a JSON file."""
    with open(filename) as f:
        return json.load(f)


@app.route("/")
def index():
    stations = load_stations("stations.json")
    return render_template("index.html", regions=stations.keys())


@app.route("/find_lowest_tides", methods=["POST"])
def find_lowest_tides():
    region = request.form["region"]
    daterange = request.form["daterange"]
    num_of_results = int(request.form["num_of_results"])

    # Split the date range into start and end dates
    start_date, end_date = daterange.split(" - ")

    # Convert dates to the correct format (yyyyMMdd)
    start_date = datetime.strptime(start_date, "%m/%d/%Y")
    end_date = datetime.strptime(end_date, "%m/%d/%Y")

    # Enforce the maximum date range of 31 days
    if (end_date - start_date).days > 31:
        return "Date range cannot exceed 31 days.", 400

    start_date = start_date.strftime("%Y%m%d")
    end_date = end_date.strftime("%Y%m%d")

    # Enforce the minimum and maximum number of results
    if num_of_results < 1 or num_of_results > 25:
        return "Number of results must be between 1 and 25.", 400

    stations = load_stations("stations.json")
    if region not in stations:
        return "Invalid region. Exiting.", 400

    lowest_tides = get_lowest_tides(
        stations, region, start_date, end_date, num_of_results
    )

    if not lowest_tides:
        return "No tide data found for the selected region and date range.", 404

    map_html = create_map(lowest_tides)
    return render_template(
        "results.html", lowest_tides=lowest_tides, region=region, map_html=map_html
    )


def get_lowest_tides(stations, region, start_date, end_date, num_of_results):
    """Fetches the lowest tides for all stations in the region."""
    station_lows = []

    def fetch_data_for_station(station_id):
        print(f"Fetching data for station: {station_id}")
        station = fetch_station_metadata(station_id)
        if station["lat"] is None or station["lon"] is None:
            print(f"Skipping station {station_id} due to missing metadata.")
            return
        predictions = fetch_tide_data(station, start_date, end_date)
        if predictions:
            lowest_tide = min(predictions, key=lambda x: float(x["v"]))
            station_name = station["name"]
            # Convert time to 12-hour format with AM/PM
            lowest_tide["time"] = datetime.strptime(
                lowest_tide["t"], "%Y-%m-%d %H:%M"
            ).strftime("%Y-%m-%d %I:%M %p")
            station_lows.append(
                {
                    "station_name": station_name,
                    "value": lowest_tide["v"],
                    "time": lowest_tide["time"],
                    "lat": station["lat"],
                    "lon": station["lon"],
                }
            )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_data_for_station, station_id)
            for station_id in stations[region]
        ]
        concurrent.futures.wait(futures)

    station_lows.sort(key=lambda x: float(x["value"]))
    return station_lows[:num_of_results]


def fetch_tide_data(station, start_date, end_date):
    """Fetches tide data from the NOAA Tides and Currents API."""
    print(f"Station data: {station}")
    api_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={start_date}&end_date={end_date}&station={station['id']}&product=predictions&datum=MLLW&units=english&time_zone=lst_ldt&application=web_services&format=json"
    print(f"Fetching tide data from URL: {api_url}")
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "predictions" in data:
            return data["predictions"]
        else:
            print(f"No predictions found in response for station {station['id']}")
    else:
        print(
            f"Failed to fetch data for station {station['id']}: {response.status_code} - {response.text}"
        )
    return []


def fetch_station_metadata(station_id):
    """Fetches station metadata from the NOAA Tides and Currents API."""
    api_url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station_id}.json"
    print(f"Fetching station metadata from URL: {api_url}")
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "stations" in data:
            station = data["stations"][0]
            return {
                "id": station_id,
                "name": station["name"],
                "lat": station["lat"],
                "lon": station["lng"],
            }
        else:
            print(f"No metadata found for station {station_id}")
    else:
        print(
            f"Failed to fetch metadata for station {station_id}: {response.status_code} - {response.text}"
        )
    return {"id": station_id, "name": f"Station {station_id}", "lat": None, "lon": None}


def create_map(lowest_tides):
    """Creates a map with markers for the lowest tides."""
    if not lowest_tides:
        return None

    map_center = [lowest_tides[0]["lat"], lowest_tides[0]["lon"]]
    tide_map = folium.Map(location=map_center, zoom_start=10)

    for tide in lowest_tides:
        folium.Marker(
            location=[tide["lat"], tide["lon"]],
            popup=f"{tide['station_name']}: {tide['value']} feet at {tide['time']}",
        ).add_to(tide_map)

    return tide_map._repr_html_()
