import configparser
import os
import math
import warnings
import pandas as pd
from math import *
from pulp import *
from itertools import *
from cafevisit.inputs import parameters
pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']
DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_RESULTS = os.path.join(BASE_PATH, '..', 'results', 'final')

path = os.path.join(DATA_RAW, 'countries.csv')
countries = pd.read_csv(path, encoding = 'latin-1')

def haversine_distance(lat1, lon1, lat2, lon2):

    """
    Given two locations, the function 
    calculate the distance between them.
    Parameters
    ----------
    lat1 : float
        Latitide of the first location
    lon1 : float
        Longitude of the first location
    lat2 : float
        Latitide of the second location
    lon2 : float
        Longitude of the second location

    Returns
    -------
    hav_distance_km : float
        The haversine distance between 
        two points in kilometers.
    """
    radius = 6371
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    hav_distance_km = round((radius * c), 4)


    return hav_distance_km


def access_cost(distance_km):
    """
    This function calculates 
    the access cost from customer 
    location to the EV service center

    Parameters
    ----------
    distance_km : float
        Haversine distance between customer 
        and EV service center location.

    Returns
    -------
    access_cost : float
        The total access cost from 
        customer to EV service center 
        in US$.
    
    """
    for key, item in parameters.items(): 

        access_cost = round(item['electricity_unit_price'] * (distance_km 
                      / item['consumption_ev']), 4)
        
    return access_cost


def linear_problem(iso3):

    """
    This function minimizes the cost 
    of accessing proposed EV service 
    centers and the number to be 
    constructed while ensuring 
    every customer is covered

    Parameters
    ----------
    iso3 : string
        Country iso3 to be processed.

    Returns
    -------
    transport_costs_dict : dict
        A dictionary containing 
        the cost of accessing 
        each EV service center 
        by customers.
    """
    customer = os.path.join(DATA_RESULTS, iso3, '{}_customers.csv'.format(iso3))
    ev_centers = os.path.join(DATA_RESULTS, iso3, '{}_ev_centers.csv'.format(iso3))
    region = os.path.join(DATA_RESULTS, iso3, '{}_region.csv'.format(iso3))
    df = pd.read_csv(customer)
    df1 = pd.read_csv(ev_centers)
    df2 = pd.read_csv(region)
    for key, item in parameters.items():

        cost_ev_center = item['cost_of_ev_center'] * item['area_of_ev_center']
        request_received = df2.demand.mean() * item['ev_spply_factor']
        # A list of EV service centers
        df1['ev_center_id'] = ['Ev_center ' + str(i) for i in range(1, 1 + df1.shape[0])]

        # Create dictionary of the EV Centers with the maximum requests they can handle.
        annual_supply_dict = {}
        for ev_service_center in df1['ev_center_id']:

            request_received = annual_supply_dict[ev_service_center] = request_received

        # Create a dictionary containing the EV service centers with the fixed supply costs
        annual_cost_dict = {}
        for ev_service_center in df1['ev_center_id']:

            cost_ev_center = annual_cost_dict[ev_service_center] = cost_ev_center

        #Create a dictionary to store the customer id and the corresponding requests
        demand_dict = { customer : df['demand'][i] for i, customer in enumerate(df['customer_id'])} 

        transport_costs_dict = {}
        for i in range(0, df1.shape[0]):
            
            # Create a dictionary that store the distances between the i-th EV service center and all customers
            warehouse_transport_costs_dict = {}
            
            # For each customer location
            for j in range(0, df.shape[0]):
                
                # Distance in Km between EV service center i and customer j
                d = 0 if df1.admin_name[i] == df.admin_name[j] else haversine_distance(
                    df1.latitude[i], df1.longitude[i], df.latitude[j], df.longitude[j])
                
                # Update costs for EV service center i
                warehouse_transport_costs_dict.update({df.customer_id[j]: access_cost(d)})
            
            # Final dictionary with all costs for all EV service centers
            transport_costs_dict.update({df1.ev_center_id[i]: warehouse_transport_costs_dict})

        lp_problem = LpProblem('CFLP', LpMinimize)

        #Build or do not built EV service center at location j (cj)
        built_ev_center = LpVariable.dicts('build_ev_center', df1['ev_center_id'], 0, 1, LpBinary)

        #Number of customers taking cars to EV service center j (v_ij)
        served_customer = LpVariable.dicts('Link', 
                        list(product(df['customer_id'], 
                        df1['ev_center_id'])), 0)
        
        #Objective Function
        annual_cost_terms = [annual_cost_dict.get(j, 0) * built_ev_center[j] for j in df1['ev_center_id']]
        transport_cost_terms = [transport_costs_dict[j][i] * served_customer[(i, j)]
            for j in df1['ev_center_id']
            for i in df['customer_id']]
            
        objective = lpSum(annual_cost_terms) + lpSum(transport_cost_terms)
        lp_problem += objective

        # Costraint: the customer request must be met
        for i in df['customer_id']:

            lp_problem += lpSum(served_customer[(i, j)] for j in df1['ev_center_id']) == demand_dict[i]

        # Constraint: an EV service center cannot fullfill more requests than its limit
        for j in df1['ev_center_id']:

            customer_demand_terms = [served_customer[(i, j)] for i in df['customer_id']]
            total_demand = lpSum(customer_demand_terms)
            supply_constraint = total_demand <= annual_supply_dict.get(j, 0) * built_ev_center.get(j, 0)
            lp_problem += supply_constraint

            # Constraint: an EV service center cannot give a customer more than its request
            for i in df['customer_id']:

                for j in df1['ev_center_id']:

                    lp_problem += served_customer[(i,j)] <= demand_dict[i] * built_ev_center[j]
        
        lp_problem.solve()
        minimized_cost = round(value(lp_problem.objective), 2)

        #Store the number of EV service centers built
        for i in df1['ev_center_id']:

            if built_ev_center[i].varValue == 1:

                df1.loc[df1['ev_center_id'] == i, 'build?'] = 'Yes'
                df1.loc[df1['ev_center_id'] == i, 'value'] = 1
            
            else:

                df1.loc[df1['ev_center_id'] == i, 'build?'] = 'No'
                df1.loc[df1['ev_center_id'] == i, 'value'] = 0

        converted_dict = {str(key): value for key, value in served_customer.items()}
        with open('served.json', 'w') as json_file:

            json.dump(converted_dict, json_file)

        fileout = '{}_optimized_ev_center.csv'.format(iso3)
        folder_out = os.path.join(DATA_RESULTS, iso3)
        if not os.path.exists(folder_out):

            os.makedirs(folder_out)

        path_out = os.path.join(folder_out, fileout)
        df1.to_csv(path_out, index = False)

    return print('Minimized cost: ', minimized_cost)


if __name__ == '__main__':

    for idx, country in countries.iterrows():

        #if not country['region'] == 'Sub-Saharan Africa' or country['Exclude'] == 1:   
        if not country['iso3'] == 'KEN':
            
            continue 

        linear_problem(countries['iso3'].loc[idx])