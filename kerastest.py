from keras.models import Sequential
from keras.layers import Dense, Activation


import numpy as np
x_train=np.array([[1, 2]])
y_train = np.array([5])
model = Sequential()
model.add(Dense(10, input_dim=5, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(3))
model.compile(loss='mse', optimizer='adam')
data = [x**2 for x in range(0,1000)]
data2 = [x for x in range(0,1000)]
for i in range(0, 1000):
# Train the model, iterating on the data in batches of 32 samples
    model.fit(np.array([[data2[i], data2[i], data2[i], data2[i], data2[i]]]), np.array([[data[i], data[i], data[i]]]), nb_epoch=1, batch_size=1, verbose=0)

#model.fit(np.array(X[i]), np.array(Y[i]), nb_epoch=1, batch_size=1, verbose=2)
print((model.predict(np.array([[8000, 8000, 8000, 8000, 8000]]))))