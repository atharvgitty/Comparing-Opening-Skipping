#reads the drone's GPS coordinates using pymavlink, finds the closest waypoint from a CSV file, and opens the corresponding Mission Planner .waypoints file from a different directory:
import csv
import os
from math import radians, cos, sin, asin, sqrt
from pymavlink import mavutil

# Function to calculate the distance between two GPS coordinates using the haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return R * c

# Connect to the drone and wait for GPS fix
print("Connecting to the drone...")
master = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
master.wait_heartbeat()
print("Waiting for GPS fix...")
while master.messages['GLOBAL_POSITION_INT'].lat == 0:
    continue
print("GPS fix acquired!")

# Read the drone GPS coordinates
drone_lat = float(master.messages['GLOBAL_POSITION_INT'].lat) / 1e7
drone_lon = float(master.messages['GLOBAL_POSITION_INT'].lon) / 1e7
drone_alt = float(master.messages['GLOBAL_POSITION_INT'].alt) / 1000

# Initialize the shortest distance and closest waypoint name
#not to be filled
shortest_distance = float('inf')
closest_waypoint_name = None
closest_waypoint_file = None

# Open the directory containing the CSV files
csv_directory = "/path/to/csv/directory"
for csv_file in os.listdir(csv_directory):
    if not csv_file.endswith(".csv"):
        continue

    # Open the CSV file
    with open(os.path.join(csv_directory, csv_file), 'r') as f:
        mission_planner = csv.DictReader(f)

        # Iterate over each waypoint
        for waypoint in mission_planner:
            # Read the waypoint coordinates
            waypoint_name = waypoint['name']
            waypoint_lat = float(waypoint['latitude'])
            waypoint_lon = float(waypoint['longitude'])

            # Calculate the distance between the drone GPS coordinates and the waypoint
            distance = haversine(drone_lat, drone_lon, waypoint_lat, waypoint_lon)

            # Check if this is the closest waypoint so far
            if distance < shortest_distance:
                shortest_distance = distance
                closest_waypoint_name = waypoint_name
                closest_waypoint_file = csv_file

# Open the corresponding Mission Planner .waypoints file
if closest_waypoint_name:
    filename = f"{closest_waypoint_name}.waypoints"
    directory = "/path/to/waypoints/directory"
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        print(f"Opening {filename}")
        # Open the file here
    else:
        print(f"Could not find {filename}")
else:
    print("Could not find any matching waypoints")