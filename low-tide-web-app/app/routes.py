from flask import render_template, request, redirect, url_for
import json
import requests
from datetime import datetime
import threading
import folium
from app import app


def load_stations(filename):
    """Loads station data from a JSON file."""
    with open(filename) as f:
        return json.load(f)


def fetch_station_info(station_id):
    """Fetches the station name and coordinates for a given station ID."""
    url = f"https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/{station_id}.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        station_info = data["stations"][0]
        station_name = station_info["name"].title()
        coordinates = (station_info["lat"], station_info["lng"])
        return station_name, coordinates
    return "Unknown Station", (0, 0)


def fetch_tide_data(station, start_date, end_date):
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


def get_lowest_tides(stations, region, start_date, end_date, num_of_results):
    """Fetches the lowest tides for all stations in the region."""
    station_lows = []
    total_stations = len(stations[region])
    progress_lock = threading.Lock()

    def fetch_data_for_station(station, index):
        predictions = fetch_tide_data(station, start_date, end_date)
        if predictions:
            lowest_tide = min(predictions, key=lambda x: float(x["v"]))
            station_name, coordinates = fetch_station_info(station)
            # Convert time to 12-hour format with AM/PM
            time_24h = datetime.strptime(lowest_tide["t"], "%Y-%m-%d %H:%M")
            time_12h = time_24h.strftime("%Y-%m-%d %I:%M %p")
            station_lows.append(
                {
                    "station_name": station_name,
                    "time": time_12h,
                    "value": float(lowest_tide["v"]),
                    "coordinates": coordinates,
                }
            )

    threads = []
    for i, station in enumerate(stations[region]):
        thread = threading.Thread(target=fetch_data_for_station, args=(station, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Sort the results by tide value and limit to the specified number of results
    station_lows.sort(key=lambda x: x["value"])
    return station_lows[:num_of_results]


def create_map(station_lows):
    """Creates a map with markers for the stations with the lowest tides."""
    m = folium.Map(
        location=[station_lows[0]["coordinates"][0], station_lows[0]["coordinates"][1]],
        zoom_start=10,
    )
    for station in station_lows:
        folium.Marker(
            location=station["coordinates"],
            popup=f"{station['station_name']}<br>Time: {station['time']}<br>Value: {station['value']} feet",
            tooltip=station["station_name"],
        ).add_to(m)
    return m._repr_html_()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        region = request.form["region"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        num_of_results = int(request.form["num_of_results"])

        stations = load_stations("stations.json")
        if region not in stations:
            return "Invalid region. Exiting.", 400

        lowest_tides = get_lowest_tides(
            stations, region, start_date, end_date, num_of_results
        )
        map_html = create_map(lowest_tides)
        return render_template(
            "results.html", lowest_tides=lowest_tides, region=region, map_html=map_html
        )

    stations = load_stations("stations.json")
    return render_template("index.html", regions=stations.keys())
