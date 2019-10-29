import os
import urllib
import urllib.request
from .helpers import get_working_directory

def download_data():
    print("Downloading data")
    directory = get_working_directory()
    raw_data_directory = os.path.join(directory, "raw_data")
    os.makedirs(raw_data_directory, exist_ok=True)

    url_dir = "https://github.com/codeformuenster/open-data/blob/4ca66ad36b394c220cda2805670f1ec2a7901bb6/verkehrsdaten/kfz/"
    filenames = [
        "kfzzaehlstellen2015.zip",
        "kfzzaehlstellen2016.zip",
        "kfzzaehlstellen2017.zip",
        "kfzzaehlstellen2018.zip",
        "kfzzaehlstellen2019BisAugust.zip",
    ]

    for f in filenames:
        target_filename = os.path.join(raw_data_directory, f)
        if os.path.exists(target_filename):
            print("file {} exists, skipping download".format(f))
            continue

        full_url = url_dir + f

        urllib.request.urlretrieve(full_url, target_filename)
