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
DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 'SSA')
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
    ax.tick_params(labelsize = 10)
    plt.title('Mozambique', fontdict={'fontname': 'DejaVu Sans', 'fontsize': 20, 'fontweight': 'bold'})
    legend = plt.legend(facecolor = 'white', title = 'Potential Sites', prop = {'size': 15}, loc = 'upper right')
    legend.get_title().set_fontsize(17)
    plt.tight_layout()

    filename = '{}_potential_sites.png'.format(iso3)
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
    ax.tick_params(labelsize = 10)
    plt.title('Mozambique', fontdict={'fontname': 'DejaVu Sans', 'fontsize': 20, 'fontweight': 'bold'})
    legend = plt.legend(facecolor = 'white', title = 'Potential Sites', prop = {'size': 15}, loc = 'upper right')
    legend.get_title().set_fontsize(17)
    plt.tight_layout()
    
    filename = '{}_annual_requests.png'.format(iso3)
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)

    plt.savefig(path_out, dpi = 480)

    return None


def discarded_sites(iso3):
    """
    This function plots the selected 
    and discarded warehouses.

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed. 
    """
    map_path = os.path.join(DATA_PROCESSED, iso3, 'national_outline.shp')
    ev_center = os.path.join(DATA_RESULTS, iso3, '{}_optimized_ev_center.csv'.format(iso3))
    df = pd.read_csv(ev_center)
    df = df.rename(columns = {'build?': 'build'})
    df = add_coordinates(df)

    country = gpd.read_file(map_path)
    sns.set(font_scale = 0.5)
    ax = country.plot(color = 'white', edgecolor = 'black', figsize = (10, 10))
    df.loc[df.build == 'Yes'].plot(ax = ax, marker = 'o', c = 'green', markersize = 50, label = 'Build')
    df.loc[df.build == 'No'].plot(ax = ax, marker = 'X', c = 'red', markersize = 50, label = 'Discard')
    ax.grid(b = True, which = 'minor', alpha = 0.25)
    ax.tick_params(labelsize = 10)

    plt.title('Mozambique', fontdict={'fontname': 'DejaVu Sans', 'fontsize': 20, 'fontweight': 'bold'})
    legend = plt.legend(facecolor = 'white', title = 'Decision', prop = {'size': 15}, loc = 'upper right')
    legend.get_title().set_fontsize(17)
    plt.tight_layout()

    filename = '{}_discarded_sites.png'.format(iso3)
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)
    
    plt.savefig(path_out, dpi = 480)


    return None


def ssa_sites():

    """
    This is a function to plot 
    potential EV service centers 
    and customer locations in
    Sub-Saharan Africa.
    """

    map_path = os.path.join(DATA_AFRICA, 'shapefile', 'sub_saharan_africa.shp')
    path = os.path.join(DATA_AFRICA)

    customer = os.path.join(DATA_AFRICA, 'SSA_customers.csv')
    ev_center = os.path.join(DATA_AFRICA, 'SSA_ev_centers.csv')

    df = pd.read_csv(customer)
    df1 = pd.read_csv(ev_center)

    customer_df = add_coordinates(df)
    ev_df = add_coordinates(df1)

    country = gpd.read_file(map_path)
    sns.set(font_scale = 1.5)
    ax = country.plot(color = 'white', edgecolor = 'none', figsize = (10, 10))

    customer_df.plot(ax = ax, marker = 'X', color = 'blue', 
            markersize = 1, alpha = 0.5, label = 'Customers', legend = True)

    ev_df.plot(ax = ax, marker = 'D', color = 'green', 
            markersize = 1, alpha = 0.5, label = 'Potential EV ServiceCenters',
            legend = True)

    ax.grid(b = True, which = 'minor', alpha = 0.25)
    ax.tick_params(labelsize = 10)
    plt.title('Customer and Potential EV Service Centers.', 
            font = 'DejaVu Sans', fontsize = 20)
    legend = plt.legend(facecolor = 'white', title = 'Potential Sites', prop = {'size': 17}, loc = 'upper right')
    legend.get_title().set_fontsize(15)
    plt.tight_layout()

    filename = 'SSA_potential_sites.png'
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)
    
    plt.savefig(path_out, dpi = 480)


    return None


def ssa_demand():

    """
    This functions filters and 
    groups the regions of Sub-
    Saharan Africa by calculating 
    regional demand and mean 
    latitude and longitude. 
    """
    map_path = map_path = os.path.join(DATA_AFRICA, 'shapefile', 'Africa_Boundaries.shp')

    region = os.path.join(DATA_AFRICA, 'SSA_region.csv')
    country = gpd.read_file(map_path)

    df = pd.read_csv(region)
    region_df = add_coordinates(df)

    sns.set(font_scale = 0.5)
    ax = country.plot(color = 'white', edgecolor = 'none', figsize = (10, 10))
    region_df.plot(ax = ax, column = 'demand', marker = 'o', c = 'demand', 
                   cmap = 'Paired', markersize = 500, alpha = 0.6)
    
    region_df.plot(ax = ax, marker = 'o', c = 'green', markersize = 0.05, 
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
    ax.tick_params(labelsize = 10)
    plt.title('Projected Annual Customer Requests.', 
            font = 'DejaVu Sans', fontsize = 12)
    legend = plt.legend(facecolor = 'white', title = 'Potential Sites', prop = {'size': 8})
    legend.get_title().set_fontsize(9)
    plt.tight_layout()
    
    filename = 'SSA_annual_requests.png'
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)

    plt.savefig(path_out, dpi = 480)


    return None


def ssa_demand_choropleth():
    """
    This function plots the population 
    distribution of Sub-Saharan Africa
    """
    map_path = os.path.join(DATA_AFRICA, 'shapefile', 'sub_saharan_africa.shp')
    path = os.path.join(DATA_AFRICA, 'SSA_region.csv')

    map_df = gpd.read_file(map_path)
    df = pd.read_csv(path)

    df_merged  = map_df.merge(df, left_on = 'GID_1', right_on = 'GID_1')
    gdf = gpd.GeoDataFrame(df_merged)
    gdf.set_geometry(col = 'geometry', inplace = True)

    sns.set(font_scale = 1.5)
    fig, ax = plt.subplots(1, figsize = (10, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('bottom', size = '5%', pad = 0.3)
    gdf.plot(column = 'demand', legend = True,
            cax = cax, ax = ax, edgecolor = 'none',
            legend_kwds = {'label': 'Annual Requests', 'orientation': 'horizontal'})
    ax.set_title('Average Sub-Regional Potential Annual Requests', fontsize = 20)

    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    fig_path = os.path.join(DATA_VIS, 'SSA_avg_demand.png')
    plt.savefig(fig_path, dpi = 720)


    return None


def discarded_ssa_sites():
    """
    This function plots the selected 
    and discarded warehouses.

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed. 
    """
    map_path = os.path.join(DATA_AFRICA, 'shapefile', 'Africa_Boundaries.shp')
    ev_center = os.path.join(DATA_AFRICA, 'SSA_optimized_ev_center.csv')
    df = pd.read_csv(ev_center)
    df = df.rename(columns = {'build?': 'build'})
    df = add_coordinates(df)

    country = gpd.read_file(map_path)
    sns.set(font_scale = 0.5)
    ax = country.plot(color = 'white', edgecolor = 'black', figsize = (10, 10))
    df.loc[df.build == 'Yes'].plot(ax = ax, marker = 'o', c = 'green', markersize = 1, label = 'Build')
    df.loc[df.build == 'No'].plot(ax = ax, marker = 'X', c = 'red', markersize = 1, label = 'Discard')
    ax.grid(b = True, which = 'minor', alpha = 0.25)
    ax.tick_params(labelsize = 10)

    plt.title('Selected and Discarded EV Service Centers.', 
            font = 'DejaVu Sans', fontsize = 12)
    legend = plt.legend(facecolor = 'white', title = 'Decision', prop = {'size': 8})
    legend.get_title().set_fontsize(9)
    plt.tight_layout()

    filename = 'SSA_discarded_sites.png'
    DATA_VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')
    path_out = os.path.join(DATA_VIS, filename)
    
    plt.savefig(path_out, dpi = 480)


    return None


if __name__ == '__main__':

    countries = pd.read_csv(path, encoding = 'latin-1')
    for idx, country in countries.iterrows():

        #if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        if not country['iso3'] == 'MOZ':
            
            continue 

        #potential_sites(countries['iso3'].loc[idx])
        #average_demand(countries['iso3'].loc[idx])
        #discarded_sites(countries['iso3'].loc[idx])

    #ssa_sites()
    #ssa_demand()
    #discarded_ssa_sites()
    ssa_demand_choropleth()