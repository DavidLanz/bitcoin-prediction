from ..data.load import load_csv
from ..data.sets import prepare_data_lstm
import numpy as np
import h5py
from keras.models import load_model

# prepare the training and test set
df = load_csv("data/all_time_close.csv")
dataset, sc, X_train, X_test, y_train, y_test = prepare_data_lstm(df, 1, 0.2)
regressor = load_model(filepath="models/01_with_mae.h5")

# predict
predicted_train = regressor.predict(X_train)
predicted_test = regressor.predict(X_test)

one_day_predict = regressor.predict(np.asarray([[y_test[-1]]]))
print("Last closing price: %.2f US Dollar" %
      sc.inverse_transform(y_test)[-1][0])
print('Predicted next closing price: %.2f US Dollar ' %
      sc.inverse_transform(one_day_predict).flatten()[0])
