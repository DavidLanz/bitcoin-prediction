from src.data.load import load_csv
from src.data.sets import training_set, calc_test_size, test_set
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from keras.preprocessing import sequence
from keras.models import load_model
from keras.layers import Dense
from keras.layers import Input, LSTM
from keras.models import Model
import h5py
import math
from sklearn.metrics import mean_squared_error

BATCH_SIZE = 64
EPOCHS = 120
TIME_STEPS = 30
TEST_SIZE = 0.2

df = load_csv("./data/all_time.csv")
X_train, y_train = training_set(df, BATCH_SIZE, TEST_SIZE, TIME_STEPS)

inputs_1_mae = Input(batch_shape=(BATCH_SIZE, TIME_STEPS, 1))
lstm_1_mae = LSTM(10, stateful=True, return_sequences=True)(inputs_1_mae)
lstm_2_mae = LSTM(10, stateful=True, return_sequences=True)(lstm_1_mae)
output_1_mae = Dense(units=1)(lstm_2_mae)
regressor_mae = Model(inputs=inputs_1_mae, outputs=output_1_mae)
regressor_mae.compile(optimizer='adam', loss='mae')
for i in range(EPOCHS):
    print("Epoch: " + str(i))
    regressor_mae.fit(X_train, y_train, shuffle=False,
                      epochs=1, batch_size=BATCH_SIZE)
    regressor_mae.reset_states()

X_test, test_set, sc = test_set(df, BATCH_SIZE, TIME_STEPS, X_train)
predicted_mae = regressor_mae.predict(X_test, batch_size=BATCH_SIZE)
regressor_mae.reset_states()

predicted_mae = np.reshape(
    predicted_mae, (predicted_mae.shape[0], predicted_mae.shape[1]))
predicted_mae = sc.inverse_transform(predicted_mae)

padded_train_size = len(X_train) + TIME_STEPS * 2
testset_length = calc_test_size(
    len(df), BATCH_SIZE, TIME_STEPS, padded_train_size)

y_test = []
for j in range(0, testset_length - TIME_STEPS):
    y_test = np.append(y_test, predicted_mae[j, TIME_STEPS - 1])

y_test = np.reshape(y_test, (y_test.shape[0], 1))

rmse = math.sqrt(mean_squared_error(
    test_set[TIME_STEPS:len(y_test)], y_test[0:len(y_test) - TIME_STEPS]))
print("RMSE:", rmse)

regressor_mae.save(filepath="models/01_with_mae.h5")
