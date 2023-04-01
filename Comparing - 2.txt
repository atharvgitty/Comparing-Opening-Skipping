#Code to compare specific rows and columns of multiple csv files stored in a directory and drone coordinates and return file which has the shortest distance with the drone coordinates
#Specify Path To CSV Files
from pymavlink import mavutil
import csv
import os
from math import radians, sin, cos, sqrt, atan2

# drone connection
master = mavutil.mavlink_connection('udp:127.0.0.1:14550')  # example connection string
# drone GPS coordinates
msg = master.recv_match(type=['GLOBAL_POSITION_INT'], blocking=True)
drone_lat = msg.lat / 1e7
drone_lon = msg.lon / 1e7

# directory containing CSV files
directory = '/path/to/csv/files'

# column and row to search in the CSV files
lat_column = 0
lon_column = 1
search_row = 1

# initialize variables
shortest_distance = float('inf')
shortest_file = ''

# calculate distances between drone coordinates and each CSV coordinate
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == search_row:
                    lat = float(row[lat_column])
                    lon = float(row[lon_column])
                    lat1, lon1 = radians(drone_lat), radians(drone_lon)
                    lat2, lon2 = radians(lat), radians(lon)
                    dlat = lat2 - lat1
                    dlon = lon2 - lon1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1-a))
                    distance = 6371 * c * 1000  # distance in meters
                    if distance < shortest_distance:
                        shortest_distance = distance
                        shortest_file = filename

# do something with the shortest file (e.g. read the file or send to drone)
print(f'Shortest distance: {shortest_distance} in file: {shortest_file}')