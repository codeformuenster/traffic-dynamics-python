[![Build Status](https://travis-ci.org/codeformuenster/traffic-dynamics-python.svg?branch=master)](https://travis-ci.org/codeformuenster/traffic-dynamics-python)

# traffic-dynamics-python

This project is in pre-alpha status. The currently implemented functionality is:

    import traffic_dynamics_python as td
    td.download_data()
    td.extract_data()
    td.reformat_and_clean_data()

The the first step, zip files are downloaded to ./data_directory/raw_data/ .

In the second step zip files are extracted to ./data_directory/extracted_data .

In the third step, the extracted data is cleaned and reformatted
to one pandas Series object per traffic light, which are then stored in ./data_directory/processed_data .