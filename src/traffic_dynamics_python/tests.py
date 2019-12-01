import pickle
import numpy as np
from mean_predictor import *
from nn_predictor import *
ampel = pickle.load(
    open(
        "/home/julian/traffic-dynamics-python/data_directory/processed_data/LSA 29120 Schleifen (MQ1008).pickle",
        "rb",
    )
)

mypredictor = MeanPredictor(ampel["2016"])
prediction = mypredictor.predict(ampel["2017"].index)
mean_squared_error = np.sqrt((prediction - ampel["2017"]).pow(2).mean())
print("mean pred: {}".format(mean_squared_error))

myzeropredictor = ZeroPredictor(ampel["2016"])
zeroprediction = myzeropredictor.predict(ampel["2017"].index)
zeropredictor_mean_squared_error = np.sqrt((zeroprediction - ampel["2017"]).pow(2).mean())
print("mean pred: {}".format(zeropredictor_mean_squared_error))


mypredictor2 = MeanPredictorDoW(ampel["2016"])
mypredictor2_prediction = mypredictor2.predict(ampel["2017"].index)
mypredictor2_mean_squared_error = np.sqrt((mypredictor2_prediction - ampel["2017"]).pow(2).mean())

print("mean pred: {}".format(mypredictor2_mean_squared_error))

myNNpredictor = NNPredictor(ampel["2016"])
NNprediction = myNNpredictor.predict(ampel["2017"].index)
NNmean_squared_error = np.sqrt((NNprediction - ampel["2017"]).pow(2).mean())
print("mean pred: {}".format(NNmean_squared_error))

