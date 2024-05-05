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
    reader = geoip2.database.Reader('./GeoLite2-ASN.mmdb')
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


# Function to plot points on the map based on location information
def plot_on_map():
    current_ips = get_foreign_ip_addresses()
    current_data = []
    for i in range(len(current_ips)):
        current_data.append(get_asn_info(current_ips[i]))
    print(current_data)


    # Get the location information from the user input fields
    location = 'Cincinnati'
    geolocator = Nominatim(user_agent="map_plotter")
    location_data = geolocator.geocode(location)

    # Check if location_data is None
    if location_data is None:
        print("Error: Location not found")
        return

    # Create a Folium map centered at the specified location
    map = folium.Map(location=[0, 0], zoom_start=2, str='VikTrace')

    # Add markers for each point on the map
    for point in current_data:
        lat = point[2]
        lon = point[3]
        print("Latitude:", lat, "Longitude:", lon)  # Debugging
        folium.Marker([float(lat), float(lon)]).add_to(map)

    # Save the map as an HTML file
    map.save('map.html')
    
    # Open the map HTML file in the default web browser and embed it in the GUI
    browser_frame = ttk.Frame(root)
    browser_frame.pack(expand=True, fill='both')

    webbrowser.open('file://' + os.path.abspath('map.html'), new=1)


# Set up the tkinter GUI
root = TK.Tk()
root.geometry('800x600')
root.title('Net Scan')

TK.Label(root, text="Click to generate a geographical map of all network connections:").pack()

plot_button = TK.Button(root, text="Update Map", command=plot_on_map)
plot_button.pack()

root.mainloop()
