# **Low Tides Finder**

## **Overview**
The **Low Tides Finder** is a Python tool designed to help you identify the best tidepooling locations by finding low tides based on a specified region and timeframe. Using NOAA's Tides and Currents API, it provides accurate predictions for the lowest tides within your criteria.

---

## **How It Works**
1. **Preloaded Station Data**:  
   Since NOAA does not provide a convenient endpoint for retrieving station IDs, this tool uses a pre-scraped JSON file containing station IDs categorized by region.  
   *(Note: The station data was manually scraped and parsed, avoiding the need for a complex dynamic scraper with web drivers.)*

2. **Low Tide Predictions**:  
   The tool queries NOAA’s API to retrieve tide data for the selected region and timeframe, filtering for the lowest tide predictions.

3. **Results Breakdown**:  
   The tool displays the lowest tide times, values, and locations for your selected criteria.

---

## **Features**
- **Regional Coverage**: Supports multiple NOAA regions with preloaded station data.  
- **Timeframe Flexibility**: Search for low tides across specific start and end dates.  
- **Customizable Results**: Choose the number of lowest tide results you’d like to display.  
- **NOAA Integration**: Queries the official NOAA Tides and Currents API for accurate predictions.  

## **Interactive Inputs**
1. **Region**: Select a region from the available options (listed in the `stations.json` file).  
2. **Timeframe**: Enter the start and end dates in `YYYYMMDD` format.  
3. **Results**: Specify the number of lowest tide results you want.  

---

## **Example Workflow**

1. **Select Region**:  
   *Prompt*: *"Which region?"*  
   *Example*: `California`  

2. **Input Timeframe**:  
   *Prompt*: *"Please enter a start date (YYYYMMDD):"*  
   *Example*: `20240101`  
   *Prompt*: *"Please enter an end date (YYYYMMDD):"*  
   *Example*: `20240107`  

3. **Results Count**:  
   *Prompt*: *"How many results do you want?"*  
   *Example*: `3`  

### **Example Output**
```
One of the lowest tides in California on 2024-01-07 in WILSON COVE, SAN CLEMENTE IS. at 13:08 with a value of -0.172 feet.
One of the lowest tides in California on 2024-01-07 in Santa Monica at 13:13 with a value of -0.185 feet.
One of the lowest tides in California on 2024-01-07 in SUISUN SLOUGH ENTRANCE at 18:17 with a value of -0.198 feet.
```

---

## **Customization**
- **Updating Station Data**:  
   If NOAA's station data changes, you can regenerate the `stations.json` file using your preferred scraping method.  

- **Enhancements**:  
   If you'd like to expand functionality (e.g., incorporating weather data or surf conditions), feel free to modify the script and integrate new APIs.  

---

## **Limitations**
1. **Station Data**:  
   The tool relies on a static JSON file for station information. Changes to NOAA's regions or stations will require manual updates to the file.  

2. **Error Handling**:  
   The script assumes consistent API responses. Unexpected errors or downtime from NOAA’s API may cause interruptions.  

---

## **Acknowledgments**
- **NOAA Tides & Currents API**: [NOAA Tides API Documentation](https://api.tidesandcurrents.noaa.gov/)  
- **Tidepooling Enthusiasts**: For inspiring the creation of this tool!

---

Enjoy exploring tidepools and discovering fascinating marine life! 🐚
