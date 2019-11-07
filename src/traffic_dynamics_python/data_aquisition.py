import os
import re
import urllib
import urllib.request
import zipfile
import datetime
import pandas as pd
import collections

from .helpers import get_working_directory

filenames = [
    "kfzzaehlstellen2015.zip",
    "kfzzaehlstellen2016.zip",
    "kfzzaehlstellen2017.zip",
    "kfzzaehlstellen2018.zip",
    "kfzzaehlstellen2019BisAugust.zip",
]


def download_data():
    print("Downloading data")
    directory = get_working_directory()
    raw_data_directory = os.path.join(directory, "raw_data")
    os.makedirs(raw_data_directory, exist_ok=True)

    url_dir = "https://github.com/codeformuenster/open-data/raw/4ca66ad36b394c220cda2805670f1ec2a7901bb6/verkehrsdaten/kfz/"

    for f in filenames:
        target_filename = os.path.join(raw_data_directory, f)
        if os.path.exists(target_filename):
            print("file {} exists, skipping download".format(f))
            continue

        full_url = url_dir + f

        urllib.request.urlretrieve(full_url, target_filename)


def extract_data():
    print("Extracting data")

    directory = get_working_directory()
    # determine directory with raw zip files
    raw_data_directory = os.path.join(directory, "raw_data")
    assert os.path.exists(raw_data_directory)

    # create directory for extracted data
    extracted_data_directory = os.path.join(directory, "extracted_data")
    os.makedirs(extracted_data_directory, exist_ok=True)

    for f in filenames:
        zip_filename = os.path.join(raw_data_directory, f)
        assert os.path.exists(zip_filename)

        with zipfile.ZipFile(zip_filename, 'r') as ziparchive:
            # replacing the filename here to avoid subfolders after extraction
            for info in ziparchive.infolist():
                filename = os.path.basename(info.filename)
                if filename == "":
                    continue
                info.filename = filename
                ziparchive.extract(info, extracted_data_directory)


_file_encoding = "windows-1252"


def _date_from_filename(filename):
    return datetime.datetime.strptime(
        re.match(r"^(\d{4}_\d{2}_\d{2})_24mq[.]csv", os.path.basename(filename)).groups()[0],
        "%Y_%m_%d"
    )


def _read_traffic_csv(filename):
    """Read the traffic csv files

    This function is only a small wrapper around pandas.read_csv
    to manage the function arguments
    """
    assert os.path.isfile(filename)

    date = _date_from_filename(filename)
    if date < datetime.datetime(2018, 9, 1):
        # old file format:
        # one line for header
        # erroneous semicolon at line end
        fileformat = "old"
        skiprows = 1
        names = ["Name"] + [str(x) for x in range(25)]
    else:
        # new file format
        # 13 lines of header
        # second column in class name
        # no semicolon at line end
        fileformat = "new"
        skiprows = 13
        names = ["Name", "class"] + [str(x) for x in range(24)]

    df = pd.read_csv(
        filename,
        encoding=_file_encoding,
        delimiter=";",
        header=None,
        skiprows=skiprows,
        names=names,
        index_col=False,
    )

    if fileformat == "old":
        df.drop("24", axis=1, inplace=True)
    else:
        df.drop("class", axis=1, inplace=True)

    return df


def reformat_and_clean_data():
    """convert to pandas and handle errors

    After extraction, data exists in one csv file per day. This function
    converts it to one pickled pandas series per traffic light.
    The resulting series has the date/time as index and the
    number of cars per hour as values.
    During the conversion procedure, data is cleaned.
    """
    directory = get_working_directory()
    extracted_data_directory = os.path.join(directory, "extracted_data")
    assert os.path.exists(extracted_data_directory)

    processed_data_directory = os.path.join(directory, "processed_data")
    os.makedirs(processed_data_directory, exist_ok=True)

    files = [f for f in os.listdir(extracted_data_directory) if f.endswith(".csv")]
    files.sort()

    # seriescollection is a dictionary, which contains
    # a list of pandas Series objects for each traffic light
    seriescollection = collections.defaultdict(list)
    for f in files:
        filename = os.path.join(extracted_data_directory, f)
        df = _read_traffic_csv(filename)

        dateobj = _date_from_filename(filename)

        # sometimes, there is different data for the same name
        # this makes to sense, so we drop them all
        df.drop_duplicates(
            subset="Name",  # drop multiple lines for the same traffic light
            keep=False,  # keep none of them
            inplace=True
        )

        # convert the name to the index
        # we cannot do this right away because of malformed csv files for years 2015 to 2018
        # there is a semicolon an each line end
        df.set_index("Name", inplace=True)

        # there are rows in the files which contain less than 24 values
        # we do not know to which hours the present values belong,
        # so we drop them all
        df.dropna(inplace=True)

        # transpose it, so we have one column for each traffic light
        df = df.T

        # just make sure nothing strange happens
        assert len(df) == 24

        # create a new datetime index
        new_index = pd.date_range(dateobj, periods=24, freq="H")
        df.set_index(new_index, inplace=True)

        # store all columns away, sorted by traffic light name
        for light_name in df.columns:
            seriescollection[light_name].append(df[light_name])

    for light_name, series_list in seriescollection.items():
        # join all the Series objects for this traffic light
        fullseries = pd.concat(series_list)
        fullseries.sort_index(inplace=True)

        target_filename = os.path.join(processed_data_directory, light_name + ".pickle")
        fullseries.to_pickle(target_filename)

        target_filename = os.path.join(processed_data_directory, light_name + ".csv")
        fullseries.to_csv(target_filename, header=True)
