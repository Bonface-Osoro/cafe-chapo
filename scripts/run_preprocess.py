import configparser
import os
import warnings
import pandas as pd
from cafechapo.preprocess import ProcessCountry, ProcessRegions, ProcessPopulation
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


path = os.path.join(DATA_RAW, 'countries.csv')
pop_tif_loc = os.path.join(DATA_RAW, 'WorldPop', 'poverty.tiff')

countries = pd.read_csv(path, encoding = 'latin-1')

for idx, country in countries.iterrows():
        
    if not country['iso3'] == 'KEN':
        
        continue 

    country = ProcessCountry(path, countries['iso3'].loc[idx])
    #country.process_country_shapes()

    regions = ProcessRegions(countries['iso3'].loc[idx], countries['gid_region'].loc[idx])
    #regions.process_regions()

    populations = ProcessPopulation(path, countries['iso3'].loc[idx], countries['gid_region'].loc[idx], pop_tif_loc)
    populations.process_national_population()
    #populations.generate_population_csv()