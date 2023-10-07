import os
import configparser
import warnings
import pandas as pd
import matplotlib.pyplot as plt 
import geopandas as gpd
from shapely import wkt
from mpl_toolkits.axes_grid1 import make_axes_locatable
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results')
DATA_VIS = os.path.join(BASE_PATH, '..', 'vis')

map_path = os.path.join(DATA_RESULTS, 'processed', 'KEN', 'regions', 'regions_1_KEN.shp')
path = os.path.join(DATA_RESULTS, 'final', 'KEN', 'population', 'KEN_population_results.csv')

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
         cax = cax, ax = ax,
         legend_kwds = {'label': 'Population', 'orientation': 'horizontal'})
ax.set_title('Kenyan Population Distribution')

fig_path = os.path.join(DATA_VIS, 'figures', 'kenya_population.png')
plt.savefig(fig_path, dpi = 720)
plt.show()