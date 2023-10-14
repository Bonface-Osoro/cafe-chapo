import os
import configparser
import warnings
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
import seaborn as sns
from shapely import wkt
from pulp import *
from itertools import *
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


def get_served_customers(inpu_ev_center, iso3):
    """
    This function find the customer ids 
    served by input EV service center

    Parameters
    ----------
    inpu_ev_center : string
        EV service center id
    iso3 : string
        Country iso3 to be processed.
    
    Returns
    -------
    linked_customers : list
        List of customer's ids connected 
        to the EV service center
    """
    customer = os.path.join(DATA_RESULTS, iso3, '{}_customers.csv'.format(iso3))
    ev_centers = os.path.join(DATA_RESULTS, iso3, '{}_ev_centers.csv'.format(iso3))
    df = pd.read_csv(customer)
    df1 = pd.read_csv(ev_centers)
    
    served_customers = LpVariable.dicts(
    'Link', [(i,j) for i in df['customer_id'] for j in df1['ev_center_id']], 0)
    
    linked_customers = []
    for (k, v) in served_customers.items():
        print(v)
        if k[1] == inpu_ev_center and v.varValue > 0:
            
            linked_customers.append(k[0])


    return linked_customers


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


def average_demand(iso3):

    """
    This functions filters and 
    groups the regions of the 
    country by calculating regional 
    demand and mean latitude and 
    longitude.

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed. 
    """
    map_path = os.path.join(DATA_PROCESSED, iso3, 'national_outline.shp')
    path = os.path.join(DATA_RESULTS, 'final', iso3)

    region = os.path.join(DATA_RESULTS, iso3, '{}_region.csv'.format(iso3))

    country = gpd.read_file(map_path)

    df = pd.read_csv(region)
    region_df = add_coordinates(df)

    sns.set(font_scale = 0.5)
    ax = country.plot(color = 'white', edgecolor = 'black', figsize = (10, 10))
    region_df.plot(ax = ax, column = 'demand', marker = 'o', c = 'demand', 
                   cmap = 'Paired', markersize = 1000, alpha = 0.6)
    
    region_df.plot(ax = ax, marker = 'o', c = 'green', markersize = 15, 
                   alpha = 0.8, label = 'Customer Location')
    
    for i, row in region_df.iterrows():

        plt.annotate(row.admin_name, xy = (row.longitude, 
                                       row.latitude + 0.2), horizontalalignment = 'center')
        
    colorbar = plt.colorbar(ax.get_children()[1], ax = ax, label = 'Annual Requests', 
                 fraction = 0.04, pad = 0.03, orientation = 'horizontal') 
    colorbar.ax.get_yaxis().label.set_fontsize(8) 
    colorbar.ax.tick_params(labelsize = 8)
    colorbar.set_label('Annual Requests', size = 10)
    
    ax.grid(b = True, which = 'minor', alpha = 0.25)
    plt.title('Projected Annual Customer Requests.', 
            font = 'Calibri Light', fontsize = 12)
    legend = plt.legend(facecolor = 'white', title = 'Potential Sites')
    legend.get_title().set_fontsize(9)
    plt.tight_layout()
    
    filename = '{}_annual_requests.jpg'.format(iso3)
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)

    plt.savefig(path_out, dpi = 480)

    return None


def linked_customers(iso3):

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
    ev_center = os.path.join(DATA_RESULTS, iso3, '{}_optimized_ev_center.csv'.format(iso3))

    df = pd.read_csv(customer, index_col = 0)
    df1 = pd.read_csv(ev_center, index_col = 0)

    establish = df1.loc[df1['build?'] == 'Yes'] 

    country = gpd.read_file(map_path)
    sns.set(font_scale = 1.5)
    ax = country.plot(color = 'white', edgecolor = 'black', figsize = (10, 10))

    establish.plot(ax = ax, marker = 'o', c = '#0059b3', markersize = 100, label = 'EV Service Centers?')
    
    df.plot(ax = ax, marker = 'X', color= '#990000', markersize = 80, alpha = 0.8, label = 'Customer')

    for w in establish.ev_center_id:
        
        connected_customers = get_served_customers(w, iso3)
        
        for c in connected_customers:
            
            ax.plot([establish.loc[establish.ev_center_id == w].longitude, df.loc[df.customer_id == c].longitude],
            [establish.loc[establish.ev_center_id == w].latitude, df.loc[df.customer_id == c].latitude],
            linewidth = 0.8, linestyle = '--', color = '#0059b3')

    plt.title('Customer and Potential EV Service Centers.', 
            font = 'Calibri Light')
    plt.legend(facecolor = 'white', fontsize=30)

    # Remove ticks from axis
    plt.xticks([])
    plt.yticks([])

    # Show plot
    plt.show()
    '''customer_df = add_coordinates(df)
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
    
    plt.savefig(path_out, dpi = 480)'''


    return plt.show()


if __name__ == '__main__':

    countries = pd.read_csv(path, encoding = 'latin-1')
    for idx, country in countries.iterrows():

        #if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        if not country['iso3'] == 'KEN':
            
            continue 

        #potential_sites(countries['iso3'].loc[idx])
        #average_demand(countries['iso3'].loc[idx])
        linked_customers(countries['iso3'].loc[idx])