"""
Processing students' responses

@author: Jiaye Wei <jiaye.wei@epfl.ch>
@Date: 09.04.2024
"""

import gdown
from objects import *
import pandas as pd

def main():
    """

    """
    # File/Share/Publish to web, then choose csv format
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSrd8SvAGZk-_2GC18JIA9fWd6el3mpI4j5S-jCqtpIu-lRbXJIY7m8wl3Bghe_TvLgB7PJp7eH_B8D/pub?output=csv'

    df = prepare_file(url)

    info_extraction(df)

def prepare_file(url):
    """Pre-processing of students' responses, which should work for both bachelor and master students.

    Args:
        url (string): _description_

    Returns:
        df (dataframe): _description_
    """
    # Download the file from Google Drive
    csv_content = gdown.download(url, quiet=False)
    df = pd.read_csv(csv_content)

    return df   

def info_extraction(df):
    """Get information from the raw data

    Args:
        df (dataframe): _description_

        Columns interpretation
            Basic (0-4)
            0: timestamp
            1: email address
            2: first name
            3: last name
            4: SCIPER

        5 same units, 
        where each unit contains (can get these information from supervisor-form-1):
            1 col for choosing projects (only for project-based),  
            0-3 cols for grades of courses

    Returns:
        _type_: _description_
    """

    #TODO: get the number of supervisors (the number of columns of one unit!)
    num_cols = df.shape[1]
    num_cols_one_choice = int(num_cols/5) -1

    for index, row in df.iterrows():
        email = row.iloc[1]
        name = row.iloc[2] + row.iloc[3]
        sciper = row.iloc[4]

    return 0

if __name__ == "__main__":
    main()