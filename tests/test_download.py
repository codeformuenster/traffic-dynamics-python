import traffic_dynamics_python as tdp
import os


def test_download_data():
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