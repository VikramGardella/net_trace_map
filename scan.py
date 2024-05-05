import psutil
import time
import geoip2.database
import tkinter as TK
import folium
from tkinter import ttk
from folium import Map, Marker
from geopy.geocoders import Nominatim
from tkhtmlview import HTMLLabel
import webbrowser
import os


def get_network_connections():
    connections = psutil.net_connections()
    print(connections)

def get_foreign_ip_addresses():
    connections = psutil.net_connections(kind='inet')
    foreign_ips = [conn.raddr.ip for conn in connections if conn.raddr and conn.status == 'ESTABLISHED']
    foreign_ips = [ip for ip in foreign_ips if '.' in ip and '192' not in ip]
    return(foreign_ips)

def get_geolocation(ip_address):
    reader = geoip2.database.Reader('path/to/GeoLite2-City.mmdb')
    response = reader.city(ip_address)
    return response.country.name, response.city.name, response.location.latitude, response.location.longitude

def get_asn_info(ip_address):
    # Initialize GeoIP2 reader
    reader = geoip2.database.Reader('./GeoLite2-ASN.mmdb')  # Replace 'path/to/GeoLite2-ASN.mmdb' with the actual path
    reader_city = geoip2.database.Reader('./GeoLite2-City.mmdb')

    # Get ASN information for the IP address
    response = reader.asn(ip_address)

    # Extract ASN data
    asn_number = response.autonomous_system_number
    asn_organization = response.autonomous_system_organization

    # Get location information for the IP address
    location_response = reader_city.city(ip_address)
    latitude = location_response.location.latitude
    longitude = location_response.location.longitude

    return asn_number, asn_organization, latitude, longitude


def gen_coordinate_pairs(conns):
    concat = ''
    for i in range(len(conns)):
        concat += (str(conns[i][2]) + ',' + str(conns[i][3]))
        if(i != len(conns)-1):
            concat += ';'
    return(concat)



# Function to plot points on the map based on location information
def plot_on_map():
    current_ips = get_foreign_ip_addresses()
    current_data = []
    for i in range(len(current_ips)):
        current_data.append(get_asn_info(current_ips[i]))
    print(current_data)
    coords_str = gen_coordinate_pairs(current_data)
    print('concatenated coord pairs: ' + coords_str)


    # Get the location information from the user input fields
    #location = location_entry.get()
    location = 'Cincinnati'
    geolocator = Nominatim(user_agent="map_plotter")
    location_data = geolocator.geocode(location)

    # Check if location_data is None
    if location_data is None:
        print("Error: Location not found")
        return

    # Create a Folium map centered at the specified location
    #print("Center Location:", location_data.latitude, location_data.longitude)  # Debugging
    #map = folium.Map(location=[location_data.latitude, location_data.longitude], zoom_start=4)
    map = folium.Map(location=[0, 0], zoom_start=2, str='VikTrace')

    # Add markers for each point on the map
    #points = points_entry.get().split(';')  # Split input by semicolon
    points = coords_str
    print("Points:", points)  # Debugging
    for point in current_data:
        lat = point[2]
        lon = point[3]
        #lat, lon = point.split(',')  # Split latitude and longitude
        print("Latitude:", lat, "Longitude:", lon)  # Debugging
        folium.Marker([float(lat), float(lon)]).add_to(map)

    # Save the map as an HTML file
    map.save('map.html')
    
    #webbrowser.open('file://' + os.path.abspath('map.html'))

    # Open the map HTML file in the default web browser and embed it in the GUI
    browser_frame = ttk.Frame(root)
    browser_frame.pack(expand=True, fill='both')

    webbrowser.open('file://' + os.path.abspath('map.html'), new=1)

'''
    # Load the map HTML file into the Tkinter GUI
    with open('map.html', 'r') as file:
        html_content = file.read()

    # Create a Tkinter HTMLLabel widget to display the map
    html_label = HTMLLabel(root, html=html_content)
    html_label.pack(expand=True, fill='both')
'''



'''
while(True):
    current_ips = get_foreign_ip_addresses()
    current_data = []
    for i in range(len(current_ips)):
        current_data.append(get_asn_info(current_ips[i]))
    print(current_data)
    time.sleep(5)
'''

# Set up the tkinter GUI
root = TK.Tk()
root.geometry('800x600')  # Set initial size of the GUI
root.title('Net Scan')

'''
TK.Label(root, text="Enter location:").pack()
location_entry = TK.Entry(root)
location_entry.pack()
'''

TK.Label(root, text="Enter points (separate by comma):").pack()
points_entry = TK.Entry(root)
points_entry.pack()

plot_button = TK.Button(root, text="Update Map Plots", command=plot_on_map)
plot_button.pack()

root.mainloop()
