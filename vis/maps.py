import os
import configparser
import warnings
import contextily as ctx
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
DATA_PROCESS = os.path.join(BASE_PATH, '..', 'results', 'processed')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results')
DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 'SSA')
DATA_VIS = os.path.join(BASE_PATH, '..', 'vis')
path = os.path.join(DATA_RAW, 'countries.csv')

def get_regional_shapes():
    """
    Load regional shapes.

    """
    output = []

    for item in os.listdir(DATA_PROCESS):

        filename_gid2 = 'regions_2_{}.shp'.format(item)
        path_gid2 = os.path.join(DATA_PROCESS, item, 'regions', filename_gid2)

        filename_gid1 = 'regions_1_{}.shp'.format(item)
        path_gid1 = os.path.join(DATA_PROCESS, item, 'regions', filename_gid1)

        if os.path.exists(path_gid2):
            data = gpd.read_file(path_gid2)
            data['GID_id'] = data['GID_2']
            data = data.to_dict('records')

        elif os.path.exists(path_gid1):
            data = gpd.read_file(path_gid1)
            data['GID_id'] = data['GID_1']
            data = data.to_dict('records')

        else:

            print('No shapefiles for {}'.format(item))
            continue

        for datum in data:
            output.append({
                'geometry': datum['geometry'],
                'properties': {
                    'GID_1': datum['GID_id'],
                },
            })

    output = gpd.GeoDataFrame.from_features(output, crs='epsg:4326')

    return output


def plot_regions_by_geotype():
    """
    Plot population density 
    by regions.

    """
    print('Plotting population density by regions')
    regions = get_regional_shapes()
    DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 
                 'SSA', 'SSA_population_results.csv')
    
    data = pd.read_csv(DATA_AFRICA)
    n = int((len(data)))
    data['pop_density'] = round(data['pop_density'])
    data = data[['GID_1', 'pop_density']]
    regions = regions[['GID_1', 'geometry']]#[:1000]
    regions = regions.copy()

    regions = regions.merge(data, left_on = 'GID_1', right_on = 'GID_1')
    regions.reset_index(drop = True, inplace = True)

    metric = 'pop_density'
    bins = [-1, 20, 43, 69, 109, 171, 257, 367, 541, 1104, 1116]
    labels = [
        '<20 $\mathregular{km^2}$',
        '20-43 $\mathregular{km^2}$',
        '43-69 $\mathregular{km^2}$',
        '69-109 $\mathregular{km^2}$',
        '109-171 $\mathregular{km^2}$',
        '171-257 $\mathregular{km^2}$',
        '257-367 $\mathregular{km^2}$',
        '367-541 $\mathregular{km^2}$',
        '541-1104 $\mathregular{km^2}$',
        '>1104 $\mathregular{km^2}$']

    regions['bin'] = pd.cut(
        regions[metric],
        bins = bins,
        labels = labels)

    sns.set(font_scale = 0.9)
    fig, ax = plt.subplots(1, 1, figsize = (10, 10))

    base = regions.plot(column = 'bin', ax = ax, 
        cmap = 'YlOrRd', linewidth = 0.2,
        legend=True, edgecolor = 'grey')

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles[::-1], labels[::-1])

    ctx.add_basemap(ax, crs = regions.crs, source = ctx.providers.CartoDB.Voyager)

    name = 'Population Density Deciles for Sub-National Regions (n={})'.format(n)
    ax.set_title(name, fontsize = 14)

    fig.tight_layout()
    path = os.path.join(DATA_VIS, 'figures', 'region_by_pop_density.png')
    fig.savefig(path)

    plt.close(fig)


def plot_demand_per_area():
    """
    Plot demand per area 
    by regions.

    """
    print('Plotting revenue per area by regions')
    regions = get_regional_shapes()
    DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 
                 'SSA', 'SSA_customers.csv')
    
    data = pd.read_csv(DATA_AFRICA)
    n = int((len(data)) / 4)
    data['demand'] = round(data['demand'])
    data = data[['GID_1', 'demand']]
    regions = regions[['GID_1', 'geometry']]#[:1000]
    regions = regions.copy()

    regions = regions.merge(data, left_on = 'GID_1', right_on = 'GID_1')
    regions.reset_index(drop = True, inplace = True)

    metric = 'demand'
    bins = [-1, 200, 800, 1500, 3500, 8000, 16000, 20000, 25000, 
            30000, 40000, 60000, 80000, 100000]
    
    labels = ['<200', '200-800', '800-1500', '1.5-3.5k', '3.5-8k',
              '8-16k', '16-20k', '20-25k', '25-30k', '30-40k', 
              '40-60k', '60-80k', '>100k']

    regions['bin'] = pd.cut(
        regions[metric],
        bins = bins,
        labels = labels)

    sns.set(font_scale = 0.9)
    fig, ax = plt.subplots(1, 1, figsize = (10, 10))

    base = regions.plot(column = 'bin', ax = ax, 
        cmap = 'YlGnBu', linewidth = 0.2,
        legend=True, edgecolor = 'grey')

    handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles[::-1], labels[::-1])

    ctx.add_basemap(ax, crs = regions.crs, source = ctx.providers.CartoDB.Voyager)

    name = 'Average Sub-National Regional Potential Annual Requests'.format(n)
    ax.set_title(name, fontsize = 20)

    fig.tight_layout()
    path = os.path.join(DATA_VIS, 'figures', 'SSA_avg_demand.png')
    fig.savefig(path)

    plt.close(fig)


def pop_density(iso3):
    """
    This function plots the population 
    distribution of a country
    """
    map_path = os.path.join(DATA_RESULTS, 'processed', iso3, 'regions', 'regions_1_{}.shp'.format(iso3))
    path = os.path.join(DATA_RESULTS, 'final', iso3, 'population', '{}_population_results.csv'.format(iso3))

    map_df = gpd.read_file(map_path)
    df = pd.read_csv(path)

    df_merged  = map_df.merge(df, left_on = 'GID_1', right_on = 'GID_1')
    gdf = gpd.GeoDataFrame(df_merged)

    gdf.drop(columns = ['geometry_x'], inplace = True)
    gdf.rename(columns = {'geometry_y': 'geometry'}, inplace = True)
    gdf['geometry'] = gdf['geometry'].apply(wkt.loads)
    gdf.set_geometry(col = 'geometry', inplace = True)

    fig, ax = plt.subplots(1, figsize = (10, 10))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('bottom', size = '5%', pad = 0.3)
    gdf.plot(column = 'population', legend = True,
            cax = cax, ax = ax, cmap = 'terrain',
            legend_kwds = {'label': 'Population', 'orientation': 'horizontal'})
    ax.set_title('Population Distribution')

    fig_path = os.path.join(DATA_VIS, 'figures', '{}_population.png'.format(iso3))
    plt.savefig(fig_path, dpi = 720)


    return None


if __name__ == '__main__':

    countries = pd.read_csv(path, encoding = 'latin-1')
    for idx, country in countries.iterrows():

        #if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        if not country['iso3'] == 'MWI':
            
            continue 

        #pop_density(countries['iso3'].loc[idx]) 
    #ssa_pop_density() 
    #plot_regions_by_geotype() 
    plot_demand_per_area()         