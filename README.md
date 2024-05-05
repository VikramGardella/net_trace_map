# net_trace_map
A Python script that uses an "Autonomous System Number" database from GeoIP's archived databases and a Tkinter GUI to map out the geographical locations of all foreign IP addresses to which your system is currently connected. You need to run it with "SuperUser" priveleges ("sudo" = "Super-User Do") like so:

sudo python3 scan.py

You'll also need to import these Python libraries (and maybe more):

pip install tkhtmlview

pip install tkinterweb

pip install geopy

pip install geoip2

pip install psutil

On top of that, because the "GeoLite2-City.mmdb" file is 50.6 Mb and GitHub has a 25 Mb file size limit, you'll need to manually download it here (make sure to place it in the same directory as scan.py, unless you plan on updating the pathway to it when setting up the "readers"):

https://www.maxmind.com/en/accounts/1009404/geoip/downloads

