# Low Tide Web App

## Description

The Low Tide Web App allows users to find and visualize the lowest tide predictions for various regions. Users can select a region, specify a date range, and choose the number of results to display. The app fetches tide data from the NOAA Tides and Currents API and displays the results on an interactive map.

## Features

- Select a region from a predefined list.
- Specify a date range (up to 31 days).
- Choose the number of results to display (1 to 25).
- Fetch and display the lowest tide predictions for the selected region and date range.
- Interactive map with markers for the lowest tides.

![alt text](https://github.com/m3lmark/low_tides/blob/main/web_page_screenshots/web_page_inputs.png?raw=true)
![alt text](https://github.com/m3lmark/low_tides/blob/main/web_page_screenshots/web_page_results.png?raw=true)

## Requirements

- Flask
- requests
- folium

## Installation

1. Clone the repository.
2. Navigate to the `low_tide/low-tide-web-app` directory.
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```
2. Open a web browser and navigate to `http://127.0.0.1:5000`.
3. Select a region, specify a date range, and choose the number of results.
4. Click "Find Lowest Tides" to view the results on the map.

## File Structure

- __init__.py: Initializes the Flask application.
- routes.py: Contains the routes and logic for fetching and displaying tide data.
- index.html: The main page for selecting region, date range, and number of results.
- results.html: The results page displaying the lowest tides on a map.
- styles.css: Custom styles for the web app.
- `low_tide/low-tide-web-app/app/stations.json`: JSON file containing station data for various regions.

## TODO

- Highlight corresponding pin on the map when a station is clicked.
- Improve pin display formatting.
- Add a loading progress bar.
- Refine the README.
- General code polishing.
