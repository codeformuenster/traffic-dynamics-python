import traffic_dynamics_python as tdp
import os


def test_download_and_extract_data():
    tdp.download_data()
    workdir = tdp.helpers.get_working_directory()

    filenames = [
        "kfzzaehlstellen2015.zip",
        "kfzzaehlstellen2016.zip",
        "kfzzaehlstellen2017.zip",
        "kfzzaehlstellen2018.zip",
        "kfzzaehlstellen2019BisAugust.zip",
    ]

    for f in filenames:
        assert os.path.exists(
            os.path.join(
                workdir,
                "raw_data",
                f
            )
        )

    tdp.extract_data()

    files_to_check = [
        "2015_01_01_24mq.csv",
        "2016_01_01_24mq.csv",
        "2017_01_01_24mq.csv",
        "2018_01_01_24mq.csv",
        "2019_01_01_24mq.csv"
    ]

    for f in files_to_check:
        assert os.path.exists(
            os.path.join(
                workdir,
                "extracted_data",
                f
            )
        )
