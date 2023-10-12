import os
import configparser
import warnings
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
import seaborn as sns
from shapely import wkt
from mpl_toolkits.axes_grid1 import make_axes_locatable
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results', 'final')
DATA_PROCESSED = os.path.join(BASE_PATH, '..', 'results', 'processed')
path = os.path.join(DATA_RAW, 'countries.csv')

def add_coordinates(df, lat = 'latitude', lng = 'longitude'):

    assert pd.Series([lat, lng]).isin(df.columns).all()

    return gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude, df.latitude))

def potential_sites(iso3):

    """
    This is a function to plot 
    potential EV service centers 
    and customer locations.

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed.
    """

    map_path = os.path.join(DATA_PROCESSED, iso3, 'national_outline.shp')
    path = os.path.join(DATA_RESULTS, 'final', iso3)

    customer = os.path.join(DATA_RESULTS, iso3, '{}_customers.csv'.format(iso3))
    ev_center = os.path.join(DATA_RESULTS, iso3, '{}_ev_centers.csv'.format(iso3))

    df = pd.read_csv(customer)
    df1 = pd.read_csv(ev_center)

    customer_df = add_coordinates(df)
    ev_df = add_coordinates(df1)

    country = gpd.read_file(map_path)
    sns.set(font_scale = 1.5)
    ax = country.plot(color = 'white', edgecolor = 'black', figsize = (10, 10))

    customer_df.plot(ax = ax, marker = 'X', color = 'blue', 
            markersize = 20, alpha = 0.5, label = 'Customers', legend = True)

    ev_df.plot(ax = ax, marker = 'D', color = 'green', 
            markersize = 20, alpha = 0.5, label = 'Potential EV ServiceCenters',
            legend = True)

    ax.grid(b = True, which = 'minor', alpha = 0.25)
    plt.title('Customer and Potential EV Service Centers.', 
            font = 'Calibri Light')
    plt.legend(facecolor = 'white', title = 'Potential Sites')
    plt.tight_layout()

    filename = '{}_potential_sites.jpg'.format(iso3)
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)
    
    plt.savefig(path_out, dpi = 480)


    return None

if __name__ == '__main__':

    countries = pd.read_csv(path, encoding = 'latin-1')
    for idx, country in countries.iterrows():

        if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        #if not country['iso3'] == 'BDI':
            
            continue 

        potential_sites(countries['iso3'].loc[idx])