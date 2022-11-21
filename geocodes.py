#Imports
from time import sleep

import numpy as np
import requests
from geopy import distance
from tqdm import tqdm

from tools import COUNTRIES


# Get the geocode of each country : geocode:latitude,longitude,radius --> example : geocode:40.712776,-74.005974,10km
# We use nominatim APIs which is the geocoding software that powers Open Street Map
#https://gis.stackexchange.com/questions/212796/get-lat-lon-extent-of-country-from-name-using-python
def get_boundingbox_country(country, output_as='boundingbox'):
    """
    get the bounding box of a country in EPSG4326 given a country name

    Parameters
    ----------
    country : str
        name of the country in english and lowercase
    output_as : 'str
        chose from 'boundingbox' or 'center'. 
         - 'boundingbox' for [latmin, latmax, lonmin, lonmax]
         - 'center' for [latcenter, loncenter]

    Returns
    -------
    output : list
        list with coordinates as str
    """
    # create url
    url = 'http://nominatim.openstreetmap.org/search?country=' + country + '&format=json&polygon=0'
    response = requests.get(url).json()[0]

    # parse response to list
    if output_as == 'boundingbox':
        lst = response[output_as]
        output = [float(i) for i in lst]
    if output_as == 'center':
        lst = [response.get(key) for key in ['lat','lon']]
        output = [float(i) for i in lst]
    return output


def minimal_radius(country) :
    """
    get the minimal radius for a circle to encompass a country
    
    """

    latmin, latmax, lonmin, lonmax = np.array(get_boundingbox_country(country, output_as = 'boundingbox'))
    center = np.array(get_boundingbox_country(country, output_as = 'center'))
    
    # Point that we will calculate the distance to the center to define the smallest radius that encompasses the country
    extremal_points = [np.array([center[0], lonmin]), np.array([center[0], lonmax]), np.array([latmin, center[1]]), np.array([latmax, center[1]])]
    
    # Distance between these extremal points to the center
    possible_radiuses = []    
    for point in extremal_points : 
        possible_radiuses.append(distance.geodesic(point, center).km)
        
    radius = min(possible_radiuses)

    return radius

def geocode(countries) : 
    """
    generate a dictionnary of the following form {country : geocode} from a list of countries
    
    """
    
    geocode = {}
    for country in tqdm(countries) :
        if country == "Ukraine" :
            geocode[country] = "48.2289622,27.1482283,200km"
        
        else :
            country_center = get_boundingbox_country(country, output_as='center')
            geocode_country = f'{country_center[0]},{country_center[1]},{minimal_radius(country)}km'
            geocode[country] = geocode_country
            sleep (0.5)
    print ("----------------------- geocodes generated -----------------------")
    return geocode

