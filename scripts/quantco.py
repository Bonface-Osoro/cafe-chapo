import os
import configparser
import warnings
import pandas as pd
import geopandas as gpd
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results', 'final')

path = os.path.join(DATA_RAW, 'countries.csv')
countries = pd.read_csv(path, encoding = 'latin-1')

southern = ['AGO', 'ZMB', 'ZWE', 'NAM', 'BWA', 'ZAF', 'LSO', 
            'SWZ', 'MOZ', 'MWI']

central = ['CMR', 'CAF', 'TCD', 'COD', 'GNQ', 'GAB', 'STP']

eastern = ['BDI', 'COM', 'DJI', 'ERI', 'ETH', 'SWZ', 'MDG', 
           'KEN', 'MUS', 'SDN', 'SYC', 'SOM', 'SSD', 'UGA', 
           'TZA', 'RWA']

west = ['BEN', 'BFA', 'CPV', 'CIV', 'GMB', 'GHA', 'GIN', 
        'GNB', 'LBR', 'MLI', 'MRT', 'NER', 'NGA', 'SEN', 
        'SLE', 'TGO']

def csv_merger(csv_name, iso3):
    """
    This funcion read and merge 
    multiple CSV files located 
    in different folders.

    Parameters
    ----------
    csv_name : string
        Name of the file to process. it can be
        '_customers.csv', '_ev_centers.csv' or
        '_optimized_ev_centers.csv'
    iso3 : string
        Country iso3 to be processed. 
    """

    print('Merging csv files for {}'.format(iso3))
    isos = os.listdir(DATA_RESULTS)

    merged_data = pd.DataFrame()
    for iso3 in isos:

        base_directory = os.path.join(DATA_RESULTS, iso3) 

        for root, _, files in os.walk(base_directory):

            for file in files:

                if file.endswith('{}{}'.format(iso3, csv_name)):
                    
                    file_path = os.path.join(base_directory, '{}{}'.format(iso3, csv_name))
                    df = pd.read_csv(file_path)
                    df['region'] = ''

                    for i in range(len(df)):

                        if iso3 in southern:

                            df['region'].loc[i] = 'Southern'

                        elif iso3 in central:

                            df['region'].loc[i] = 'Central'

                        elif iso3 in eastern:

                            df['region'].loc[i] = 'Eastern'

                        else: 

                            df['region'].loc[i] = 'West'

                    merged_data = pd.concat([merged_data, df], ignore_index = True)

                    fileout = 'SSA{}'.format(csv_name)
                    folder_out = os.path.join(DATA_RESULTS, '..', 'SSA')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    merged_data.to_csv(path_out, index = False)

    return None


def pop_csv_merger(iso3):
    """
    This funcion read and merge 
    multiple populationCSV files 
    located in different folders.

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed. 
    """

    print('Merging csv files for {}'.format(iso3))
    isos = os.listdir(DATA_RESULTS)

    merged_data = pd.DataFrame()
    for iso3 in isos:

        base_directory = os.path.join(DATA_RESULTS, iso3, 'population') 

        for root, _, files in os.walk(base_directory):

            for file in files:

                if file.endswith('{}_population_results.csv'.format(iso3)):
                    
                    file_path = os.path.join(base_directory, '{}_population_results.csv').format(iso3)
                    df = pd.read_csv(file_path)
                    df['region'] = ''

                    for i in range(len(df)):

                        if iso3 in southern:

                            df['region'].loc[i] = 'Southern'

                        elif iso3 in central:

                            df['region'].loc[i] = 'Central'

                        elif iso3 in eastern:

                            df['region'].loc[i] = 'Eastern'

                        else: 

                            df['region'].loc[i] = 'West'

                    merged_data = pd.concat([merged_data, df], ignore_index = True)

                    fileout = 'SSA_population_results.csv'
                    folder_out = os.path.join(DATA_RESULTS, '..', 'SSA')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    merged_data.to_csv(path_out, index = False)

    return None


def generate_ssa_shapefile(iso3):
    """
    This funcion generates the 
    shapefile of Sub-Saharan Africa

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed. 
    """
    print('Merging shapefiles for {}'.format(iso3))
    isos = os.listdir(DATA_RESULTS)

    merged_data = gpd.GeoDataFrame()
    for iso3 in isos:

        base_directory = os.path.join(BASE_PATH, '..', 'results', 'processed', iso3, 'regions')

        for root, _, files in os.walk(base_directory):

            for file in files:

                if file.endswith('{}.shp'.format(iso3)):

                    file_path = os.path.join(base_directory, 'regions_2_{}.shp').format(iso3)
                    file_path_1 = os.path.join(base_directory, 'regions_1_{}.shp').format(iso3)
                    if os.path.exists(file_path):

                        df = gpd.read_file(file_path)
                        
                    else:

                        df = gpd.read_file(file_path_1)

                    merged_data = pd.concat([merged_data, df], ignore_index = True)

                    fileout = 'sub_saharan_africa.shp'
                    folder_out = os.path.join(DATA_RESULTS, '..', 'SSA', 'shapefile')

                    if not os.path.exists(folder_out):

                        os.makedirs(folder_out)

                    path_out = os.path.join(folder_out, fileout)
                    merged_data.to_file(path_out, driver = 'ESRI Shapefile')

    return None


def case_countries(selected_countries):
    """
    This function aggregates results for 
    four selected countries for the case 
    study

    Parameters
    ----------
    selected_countries : list
        List of countries selected. 
    """
    DATA_AFRICA = os.path.join(BASE_PATH, '..', 'results', 'SSA')
    csv_data = os.path.join(DATA_AFRICA, 'SSA_optimized_ev_center.csv')
    df = pd.read_csv(csv_data)
    df = df[df['iso3'].isin(selected_countries)]

    fileout = 'four_countries.csv'
    folder_out = os.path.join(DATA_AFRICA)

    if not os.path.exists(folder_out):

        os.makedirs(folder_out)

    path_out = os.path.join(folder_out, fileout)
    df.to_csv(path_out, index = False)


    return None


if __name__ == '__main__':

    for idx, country in countries.iterrows():

        if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        #if not country['iso3'] == 'BEN':
            
            continue 

        csv_merger('_customers.csv', countries['iso3'].loc[idx])
        csv_merger('_ev_centers.csv', countries['iso3'].loc[idx])
        csv_merger('_optimized_ev_center.csv', countries['iso3'].loc[idx])
        csv_merger('_region.csv', countries['iso3'].loc[idx])
        pop_csv_merger(countries['iso3'].loc[idx])
        #generate_ssa_shapefile(countries['iso3'].loc[idx])

selected_countries = ['KEN', 'GHA', 'CMR', 'MOZ']
#case_countries(selected_countries)