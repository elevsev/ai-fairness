# Route Optimizer

A Streamlit web application that helps users find the optimal route between multiple locations. The application uses the Traveling Salesman Problem (TSP) algorithm to find the most efficient route and displays it on an interactive map.

## Features

- Add multiple locations by address
- Automatic geocoding of addresses
- Interactive map display
- Optimal route calculation
- Distance information
- Route visualization with markers and lines

## Setup

1. Make sure you have Python 3.8+ installed
2. Clone this repository
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Activate the virtual environment if not already activated:
   ```bash
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. The application will open in your default web browser

## Usage

1. Enter an address in the text input field
2. Click "Add Location" to add it to your route
3. Repeat steps 1-2 for all locations you want to include
4. Click "Calculate Optimal Route" to see the best route between all locations
5. The map will show the route with markers for each location
6. Route information including total distance will be displayed below the map

## Notes

- The application uses the Nominatim geocoding service, which has usage limits
- Addresses should be as specific as possible for accurate results
- The route optimization uses an approximation algorithm for the Traveling Salesman Problem 