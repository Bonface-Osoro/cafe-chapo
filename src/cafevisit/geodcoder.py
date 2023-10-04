import configparser
import os 
import warnings
import pandas as pd
from geopy.geocoders import Nominatim
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results')

def geocoding(iso3):
    '''
    This function reads the population csv file 
    and geocodes the region names with a central 
    coordinate.

    Parameters
    ----------
    iso3 : iso3
        Country Iso3 name.
    '''
    nom = Nominatim(timeout = 10, user_agent = 'kinyanjuicarringtone@gmail.com') #set your email address
    pop_folder = os.path.join(DATA_RESULTS, 'final', iso3, 'population')
    filename = '{}_population_results.csv'.format(iso3)
    file_input = os.path.join(pop_folder, filename)


    df = pd.read_csv(file_input)
    df[['coordinates', 'latitude', 'longitude']] = ''

    print('Geocoding {}'.format(iso3))
    df.coordinates = df['NAME_1'].apply(nom.geocode)

    df['latitude'] = df['coordinates'].apply(lambda x: x.latitude)
    df['longitude'] = df['coordinates'].apply(lambda x: x.longitude)
    df = df.drop(['coordinates'], axis = 1)

    fileout = '{}_location_results.csv'.format(iso3)
    folder_out = os.path.join(DATA_RESULTS, 'final', iso3, 'population')

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)

    df.to_csv(path_out, index = False)

    return None