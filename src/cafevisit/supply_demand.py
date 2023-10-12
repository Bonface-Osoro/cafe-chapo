import configparser
import os
import geopandas as gpd
import numpy as np
import pandas as pd

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results', 'final')

#pop = os.path.join(DATA_RESULTS, )

class SupplyDemand:

    """
    This class process the supply by the EV service centers and 
    potential demand from customers.
    """

    def __init__(self, country_iso3):
        """
        A class constructor

        Arguments
        ---------
        country_iso3 : string
            Country iso3 to be processed.
        """
        self.country_iso3 = country_iso3

    def customer_ev_centers(self):

        """
        This function creates a 
        dataframe of potential 
        customers and EV centers
        """
        random_state = 2
        fraction_customers = 0.9
        fraction_ev_centers = 0.3
        demand_fraction = 0.02

        pop = os.path.join(DATA_RESULTS, self.country_iso3, 
                           'population', '{}_population_results.csv'.format(self.country_iso3))
        df = pd.read_csv(pop)
        
        region_list = df['region'].unique().tolist()
        df['demand'] = np.floor(demand_fraction * df.population + 
                       np.random.uniform(-10, 10, size = (df.shape[0],)))
        
        ev_df = df.loc[df.region.isin(region_list)].sample(
            frac = fraction_ev_centers, random_state = random_state).reset_index()
        
        customer_df = df.loc[df.region.isin(region_list)].sample(
            frac = fraction_customers, random_state = random_state).reset_index()
        
        ev_name = '{}.shp'.format(self.country_iso3)    

        ev_name = '{}_ev_centers.csv'.format(self.country_iso3)
        customer_name = '{}_customers.csv'.format(self.country_iso3)

        folder_out = os.path.join(DATA_RESULTS, self.country_iso3)

        if not os.path.exists(folder_out):

            os.makedirs(folder_out)

        path_out = os.path.join(folder_out, ev_name)
        path_out_1 = os.path.join(folder_out, customer_name)

        ev_df.to_csv(path_out)
        customer_df.to_csv(path_out_1)

        return None
    

    def add_coordinates(df, lat = 'latitude', lng = 'longitude'):

        assert pd.Series([lat, lng]).isin(df.columns).all()

        geocoded_df = gpd.GeoDataFrame(df, 
                      geometry = gpd.points_from_xy(df.longitude, df.latitude))

        return geocoded_df