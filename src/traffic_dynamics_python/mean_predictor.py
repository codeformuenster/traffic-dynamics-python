#   use:
#   mypredictor = mean_predictor(trainingdata as series)
#   myprediction = mypredictor.predict(index of testdata) (where testdata is a series)
#   error = myprediction - testdata
#   meansquarederror = error.pow(2).mean()

import pandas as pd

class ZeroPredictor:
    def __init__(self, series):
        assert isinstance(series, pd.Series)

    def predict(self, test_index):
        assert isinstance(test_index, pd.DatetimeIndex)
        prediction = [0. for x in test_index.hour]
        return pd.Series(prediction, test_index)


class MeanPredictor:
    def __init__(self, series):
        assert isinstance(series, pd.Series)
        train_data = pd.DataFrame(series)
        train_data["hour"] = train_data.index.hour
        self.mean_values = train_data.groupby("hour").mean().iloc[:, 0]

    def predict(self, test_index):
        assert isinstance(test_index, pd.DatetimeIndex)
        prediction = [self.mean_values[x] for x in test_index.hour]
        return pd.Series(prediction, test_index)


class MeanPredictorDoW:
    def __init__(self, series):
        assert isinstance(series, pd.Series)
        train_data = pd.DataFrame(series)
        train_data["hour"] = train_data.index.hour
        train_data["dow"] = train_data.index.dayofweek
        self.mean_values = train_data.groupby(["dow", "hour"]).mean().iloc[:, 0]

    def predict(self, test_index):
        assert isinstance(test_index, pd.DatetimeIndex)
        prediction = [self.mean_values[x] for x in zip(test_index.dayofweek, test_index.hour)]
        return pd.Series(prediction, test_index)



