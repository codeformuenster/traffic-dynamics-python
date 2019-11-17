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

    # test extract data
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

    # test cleanup of data
    tdp.reformat_and_clean_data()

    # some tests, manually constructed:
    
    import pickle
    import numpy as np
    test_trafficlight_filename = os.path.join(tdp.helpers.get_working_directory(), "processed_data", "LSA 29120 Schleifen (MQ1008).pickle")
    test_trafficlight = pickle.load(open(test_trafficlight_filename,"rb"))
    
    mean_predictor = tdp.MeanPredictor(test_trafficlight["2016"])
    mean_prediction = mean_predictor.predict(test_trafficlight["2017"].index)
    mean_predictor_mse = np.sqrt((mean_prediction - test_trafficlight["2017"]).pow(2).mean())
    assert abs(mean_predictor_mse - 294.8)<1

    zero_predictor = tdp.ZeroPredictor(test_trafficlight["2016"])
    zero_prediction = zero_predictor.predict(test_trafficlight["2017"].index)
    zero_predictor_mse = np.sqrt((zero_prediction - test_trafficlight["2017"]).pow(2).mean())
    assert abs(zero_predictor_mse - 890.8)<1
    
    mean_dow_predictor = tdp.MeanPredictorDoW(test_trafficlight["2016"])
    mean_dow_prediction = mean_dow_predictor.predict(test_trafficlight["2017"].index)
    mean_dow_predictor_mse = np.sqrt((mean_dow_prediction - test_trafficlight["2017"]).pow(2).mean())
    assert abs(mean_dow_predictor_mse - 227.7)<1
