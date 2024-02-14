import requests
from pyorbital.orbital import Orbital
from datetime import datetime
from tqdm import tqdm

### Config, user may change these =====================================================================================
time = datetime(2024, 2, 14, 21, 20, 15)   #YYYY MM DD HH MM SS, in UTC, omit leading zeros
latitude = 12.3456    #latitude of groundstation, south is negative
longitude = -12.3456	#longitude of groundstation, west is negative
altitude = 0      #elevation of groundstation above zero, in meters
target_az = 180	    #if you know where you were pointed, set rough azimuth here
target_el = 45	    #if you know where you were pointed, set rough elevation here
tolerance_az = 50   #search this many degrees around the target azimuth
tolerance_el = 30   #search this many degrees around the target elevation
resolution = 1      #how many digits after the comma your results should have
blacklist = ["STARLINK", "ONEWEB", "ORBCOMM"] #Exclude any satellites that contain these names
###===================================================================================================================
def checkBlacklist(name):
    for i in range(len(blacklist)):
        if blacklist[i] in name:
            return False
    return True
sats_all = []
sats_filtered = []
class Overpass:
    def __init__(self, sat_name, Azimuth, Elevation):
        self.name = sat_name
        self.azimuth = Azimuth
        self.elevation = Elevation
tle_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
open("active_sats.txt", "wb").write(requests.get(tle_url).content)
linenumber = 0
with open("active_sats.txt") as tlefile:
    while (line := tlefile.readline().rstrip()):
        if(linenumber % 3 == 0):
            if(checkBlacklist(line)):
                sats_all.append(str(line))
        linenumber += 1
failures = 0
for i in tqdm(range(len(sats_all))):
    try:
        satellite = Orbital(sats_all[i], tle_file = "active_sats.txt")
        Azimuth, Elevation = satellite.get_observer_look(time, longitude, latitude, altitude)
        if((abs(Azimuth - target_az) <= tolerance_az) and (abs(Elevation - target_el) <= tolerance_el)):
            sats_filtered.append(Overpass(sats_all[i], Azimuth, Elevation))
    except:
        failures += 1
for j in range(len(sats_filtered)):
    print(str(sats_filtered[j].name) + " Az: " + str(round(sats_filtered[j].azimuth, resolution)) + " El:" + str(round(sats_filtered[j].elevation, resolution)))
print("Checked " + str(len(sats_all) - failures) + " of " + str(len(sats_all)) + " Satellites.")
