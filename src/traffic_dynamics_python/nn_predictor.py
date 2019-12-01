#   use:
#   mypredictor = nn_predictor(trainingdata as series)
#   myprediction = mypredictor.predict(index of testdata) (where testdata is a series)
#   error = myprediction - testdata
#   meansquarederror = error.pow(2).mean()

import pandas as pd
import numpy as np
import torch

class NNPredictor:
    def __init__(self, series):
        
        model = torch.nn.Sequential (
            torch.nn.Linear(1,32),
            torch.nn.ReLU(),
            torch.nn.Linear(32,16),
            torch.nn.ReLU(),
            torch.nn.Linear(16,1))
        
        loss_fkt = torch.nn.MSELoss(reduction = "mean")
        
        x = torch.tensor(series.index.hour, dtype = torch.float32)
        x = x.reshape(len(x),1)
        
        y = torch.tensor(series)
        y = y.reshape(len(y),1)

        learning_rate = 1e-2
        optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)

        epocs = 5000 
        for i in range(epocs):
            y_pred = model(x)
            loss = loss_fkt(y_pred, y)
            if i%100 == 0:
                print("loss: %f" %(loss.item()))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        self.model = model 
        
        assert isinstance(series, pd.Series)

    def predict(self, test_index):
        input_tensor = torch.tensor(test_index.hour, dtype = torch.float32).reshape(len(test_index), 1)
        with torch.no_grad():
            y_pred = self.model(input_tensor)
        assert isinstance(test_index, pd.DatetimeIndex)
        return pd.Series(y_pred[:,0], test_index)

