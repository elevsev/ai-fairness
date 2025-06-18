import streamlit as st
import folium
from streamlit_folium import folium_static
import networkx as nx
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np

st.set_page_config(page_title="Route Optimizer", layout="wide")

st.title("🚗 Route Optimizer")
st.write("Enter multiple locations to find the optimal route between them.")

# Initialize session state for locations if it doesn't exist
if 'locations' not in st.session_state:
    st.session_state.locations = []

# Function to get coordinates from address
def get_coordinates(address):
    geolocator = Nominatim(user_agent="route_optimizer")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return None
    except:
        return None

# Function to calculate distance matrix
def calculate_distance_matrix(coordinates):
    n = len(coordinates)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = geodesic(coordinates[i], coordinates[j]).kilometers
    return matrix

# Function to find optimal route using TSP
def find_optimal_route(distance_matrix):
    G = nx.Graph()
    n = len(distance_matrix)
    
    # Add edges with weights
    for i in range(n):
        for j in range(i+1, n):
            G.add_edge(i, j, weight=distance_matrix[i][j])
    
    # Find approximate TSP solution
    route = nx.approximation.traveling_salesman_problem(G, cycle=True)
    return route

# Input for new location
new_location = st.text_input("Enter a location (e.g., 'New York, NY' or '1600 Pennsylvania Ave, Washington DC'):")

if st.button("Add Location") and new_location:
    coords = get_coordinates(new_location)
    if coords:
        st.session_state.locations.append({
            'address': new_location,
            'coordinates': coords
        })
        st.success(f"Added: {new_location}")
    else:
        st.error("Could not find coordinates for this location. Please try a different address.")

# Display current locations
if st.session_state.locations:
    st.subheader("Current Locations:")
    for i, loc in enumerate(st.session_state.locations):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{i+1}. {loc['address']}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.locations.pop(i)
                st.rerun()

# Calculate and display route
if len(st.session_state.locations) >= 2:
    if st.button("Calculate Optimal Route"):
        # Extract coordinates
        coordinates = [loc['coordinates'] for loc in st.session_state.locations]
        
        # Calculate distance matrix
        distance_matrix = calculate_distance_matrix(coordinates)
        
        # Find optimal route
        route = find_optimal_route(distance_matrix)
        
        # Create map
        center_lat = sum(coord[0] for coord in coordinates) / len(coordinates)
        center_lon = sum(coord[1] for coord in coordinates) / len(coordinates)
        m = folium.Map(location=[center_lat, center_lon], zoom_start=10)
        
        # Add markers and route
        route_coords = []
        total_distance = 0
        
        for i in range(len(route)-1):
            start_idx = route[i]
            end_idx = route[i+1]
            
            start_coord = coordinates[start_idx]
            end_coord = coordinates[end_idx]
            
            # Add markers
            folium.Marker(
                start_coord,
                popup=st.session_state.locations[start_idx]['address'],
                icon=folium.Icon(color='red' if i == 0 else 'blue')
            ).add_to(m)
            
            # Add route line
            folium.PolyLine(
                [start_coord, end_coord],
                color='blue',
                weight=2,
                opacity=0.8
            ).add_to(m)
            
            # Calculate distance
            distance = geodesic(start_coord, end_coord).kilometers
            total_distance += distance
            route_coords.extend([start_coord, end_coord])
        
        # Display map
        folium_static(m)
        
        # Display route information
        st.subheader("Route Information")
        st.write(f"Total Distance: {total_distance:.2f} km")
        
        st.write("Route Order:")
        for i in range(len(route)-1):
            st.write(f"{i+1}. {st.session_state.locations[route[i]]['address']} → {st.session_state.locations[route[i+1]]['address']}")

elif len(st.session_state.locations) == 1:
    st.warning("Please add at least one more location to calculate a route.")
else:
    st.info("Add at least two locations to calculate an optimal route.") 