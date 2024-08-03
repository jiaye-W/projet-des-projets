import requests
import pandas as pd

# Useful method for print out dictionary
def print_dict_items(dictionary):
    """
    Print each item of the dictionary one per line.
    
    Parameters:
    dictionary (dict): The dictionary to print.
    """
    for key, value in dictionary.items():
        print(f"{key}: {value}")

def download_and_process_csv(url):
    """
    Downloads a CSV file from the given URL, saves it locally,
    reads it into a pandas DataFrame, and returns the DataFrame.

    Parameters:
    url (str): The URL of the CSV file.

    Returns:
    pd.DataFrame: The DataFrame containing the CSV data.
    """
    # Send a HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create a file name based on the URL
        file_name = url.split("/")[-1]

        # Save the content of the response to a file
        with open(file_name, 'wb') as file:
            file.write(response.content)

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_name)

        return df
    else:
        print(f"Failed to download the file from {url}")
        return None
    
def compute_total_number_of_projects(project_capacities):
    number_projects = 0
    for key, value in project_capacities.items():
        number_projects += value
    return number_projects