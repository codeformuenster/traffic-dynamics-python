import os
import urllib
import urllib.request
import zipfile
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
