import configparser
import os
import geopandas as gpd
import numpy as np
import pandas as pd
from cafevisit.inputs import parameters

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
        for key, item in parameters.items():

            print('Generating demand and supply results for {}'.format(self.country_iso3))
            pop = os.path.join(DATA_RESULTS, self.country_iso3, 
                            'population', '{}_population_results.csv'.format(self.country_iso3))
            df = pd.read_csv(pop)
            
            region_list = df['admin_name'].unique().tolist()
            df['demand'] = np.floor(item['demand_fraction'] * df.population + 
                        np.random.uniform(-10, 10, size = (df.shape[0],)))
            
            ev_df = df.loc[df.admin_name.isin(region_list)].loc[df.capital.isin(
                ['admin', 'minor'])].sample(frac = item['fraction_ev_centers'], 
                random_state = item['random_state'], ignore_index = True)
            
            ev_df['ev_center_id'] = range(1, 1 + ev_df.shape[0])
            
            customer_df = df.loc[df.admin_name.isin(region_list)].sample(frac = 
                        item['fraction_customers'], random_state = 
                        item['random_state'], ignore_index=True)
            
            customer_df['customer_id'] = range(1, 1 + customer_df.shape[0])
            
            region_df = df.loc[df.admin_name.isin(region_list)].groupby(['admin_name']).agg(
                {'latitude': 'mean', 'longitude': 'mean', 'demand': 'sum'}).reset_index()

            ev_name = '{}_ev_centers.csv'.format(self.country_iso3)
            customer_name = '{}_customers.csv'.format(self.country_iso3)
            region_name = '{}_region.csv'.format(self.country_iso3)

            folder_out = os.path.join(DATA_RESULTS, self.country_iso3)

            if not os.path.exists(folder_out):

                os.makedirs(folder_out)

            path_out = os.path.join(folder_out, ev_name)
            path_out_1 = os.path.join(folder_out, customer_name)
            path_out_2 = os.path.join(folder_out, region_name)

            ev_df.to_csv(path_out)
            customer_df.to_csv(path_out_1)
            region_df.to_csv(path_out_2)

        return None
    

    def add_coordinates(df, lat = 'latitude', lng = 'longitude'):

        assert pd.Series([lat, lng]).isin(df.columns).all()

        geocoded_df = gpd.GeoDataFrame(df, 
                      geometry = gpd.points_from_xy(df.longitude, df.latitude))

        return geocoded_df