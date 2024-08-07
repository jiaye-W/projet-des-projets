import requests
import pandas as pd

"""Download data from URL and processing"""

# URLs
url_supervisor_1 = 'https://sma-semester-projects.epfl.ch/export'
url_student = 'https://sma-semester-projects.epfl.ch/export_student'
url_supervisor_2 = 'https://sma-semester-projects.epfl.ch/export_results'

# 08.07.24: For the test running, we will use the csv file and don't have to download it from the url address.

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
