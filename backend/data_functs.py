import requests
import json
import pandas as pd


### Acquire national Covid data
# Ping national data API endpoint 
# Load response into JSON
# normialize JSON into dataframe
# clean data through sorting and NAN normialzation
# return df
def get_national_data():
    # Replace 'your_api_endpoint' with the actual API endpoint you want to query
    api_endpoint = 'https://api.covidtracking.com/v2/us/daily.json'

    # Make a GET request to the API
    api_response = requests.get(api_endpoint)

    # Check if the request was successful (status code 200)
    if api_response.status_code == 200:

        # try parsing and cleaning data
        try:
            # Parse the JSON data in the api_response
            json_data = api_response.json()

            # show top level keys from json response
            # print(json_data.keys())

            # Use pd.json_normalize to convert the JSON to a DataFrame
            normalized_data_df = pd.json_normalize(json_data['data'])

            # Data cleaning and sorting
                # sort by date
                # replace NAN entries with 0's
                # reset df inidicies
            normalized_data_df.sort_values(by='date', ascending=True, inplace=True)
            normalized_data_df=normalized_data_df.fillna(0)
            normalized_data_df.reset_index(inplace=True, drop=True)

            ### create list of level 1 parameters to load into listbox in toplevel script
            level_1_params=[]

            # for each column in the df (excluding the 'date' and 'states' column)
            for col in normalized_data_df.columns.values[2:]:
                
                # split column name on '.' and and first entry to list
                level_1_params.append(col.split('.')[0])

            # remove duplicates from list
            level_1_params = set(level_1_params)

            # return data that was fetched and cleaned
            return(normalized_data_df, level_1_params)
        
        # if there is an error in the parsing/cleaning process
        except:
            raise RuntimeError("Error while cleaning data.")

    # if request or data cleaning was not successful
    else:
        # Raise an error if the request was not successful
        raise RuntimeError(f"Error while fetching data from API.\n Error: {api_response.status_code}")

### Acquire States Covid data
# Ping State data API endpoint 
# Load response into JSON
# normialize JSON into dataframe
# clean data through sorting and NAN normialzation
# return df
def get_state_data(state):
    # API endpoint to query
    # state name must be lower case for API endpoint
    api_endpoint = 'https://api.covidtracking.com/v2/states/' +(state.lower())+ '/daily.json'

    # Make a GET request to the API
    api_response = requests.get(api_endpoint)

    # Check if the request was successful (status code 200)
    if api_response.status_code == 200:

        # try parsing and cleaning data
        try:
            # Parse the JSON data in the api_response
            json_data = api_response.json()

            # show top level keys from json response
            # print(json_data.keys())

            # Use pd.json_normalize to convert the JSON to a DataFrame
            normalized_data_df = pd.json_normalize(json_data['data'])

            # Data cleaning and sorting
                # sort by date
                # replace NAN entries with 0's
                # reset df inidicies
            normalized_data_df.sort_values(by='date', ascending=True, inplace=True)
            normalized_data_df=normalized_data_df.fillna(0)
            normalized_data_df.reset_index(inplace=True, drop=True)

            ### create list of level 1 parameters to load into listbox in toplevel script
            level_1_params=[]

            # for each column in the df (excluding the 'date' and 'states' column)
            for col in normalized_data_df.columns.values[2:]:
                
                # split column name on '.' and and first entry to list
                level_1_params.append(col.split('.')[0])

            # remove duplicates from list
            level_1_params = set(level_1_params)

            # filter metadata out
            level_1_params=[ent for ent in level_1_params if ent != 'meta']

            # return data that was fetched and cleaned
            # filter metadata out
            return(normalized_data_df, level_1_params)
        
        # if there is an error in the parsing/cleaning process
        except:
            raise RuntimeError("Error while cleaning data.")

    # if request or data cleaning was not successful
    else:
        # Raise an error if the request was not successful
        raise RuntimeError(f"Error while fetching data from API.\n Error: {api_response.status_code}")

# function to retrieve level 2 parameters based on level 1 selection
# @@@ add region as argument
def get_L2_params(state_data_df, l1_param_selection):

    # use selection from first listbox (L1) to filter df columns on selection
    filtered_col_names=[col for col in list(state_data_df.columns.values[2:]) if col.split('.')[0] == l1_param_selection.lower()]

    ##### create list of level 2 parameters to load into listbox in toplevel script
    level_2_params=[]

    # for each column in the filtered list
    for col in filtered_col_names:
        
        # split column name on '.' and add second entry to list
        level_2_params.append(col.split('.')[1])

    # remove duplicates from list
    level_2_params = set(level_2_params)
    return(level_2_params)