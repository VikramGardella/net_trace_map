import psutil
import time
import geoip2.database
import tkinter as TK
import folium
from geopy.geocoders import Nominatim


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

    # Get ASN information for the IP address
    response = reader.asn(ip_address)

    # Extract ASN data
    asn_number = response.autonomous_system_number
    asn_organization = response.autonomous_system_organization

    return asn_number, asn_organization


# Function to plot points on the map based on location information
def plot_on_map():
    # Get the location information from the user input fields
    location = location_entry.get()
    geolocator = Nominatim(user_agent="map_plotter")
    location_data = geolocator.geocode(location)

    # Check if location_data is None
    if location_data is None:
        print("Error: Location not found")
        return

    # Create a Folium map centered at the specified location
    print("Center Location:", location_data.latitude, location_data.longitude)  # Debugging
    map = folium.Map(location=[location_data.latitude, location_data.longitude], zoom_start=10)

    # Add markers for each point on the map
    points = points_entry.get().split(';')  # Split input by semicolon
    print("Points:", points)  # Debugging
    for point in points:
        lat, lon = point.split(',')  # Split latitude and longitude
        print("Latitude:", lat, "Longitude:", lon)  # Debugging
        folium.Marker([float(lat), float(lon)]).add_to(map)

    # Save the map as an HTML file
    map.save('map.html')



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

TK.Label(root, text="Enter location:").pack()
location_entry = TK.Entry(root)
location_entry.pack()

TK.Label(root, text="Enter points (separate by comma):").pack()
points_entry = TK.Entry(root)
points_entry.pack()

plot_button = TK.Button(root, text="Plot on Map", command=plot_on_map)
plot_button.pack()

root.mainloop()