import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Reshape
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers import Dropout
from keras.layers import MaxPooling2D
# Para usar la CPU Descomentar lo de abajo
# import os
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# model = Sequential([
#   Flatten(input_shape=(28, 28)),
#   Dense(128, activation='relu'),
#   Dense(10, activation='softmax')
# ])

# model = Sequential([
#     Reshape((28,28,1), input_shape=(28,28)),
#     Conv2D(28, kernel_size=(3,3)),
#     MaxPooling2D(pool_size=(2, 2)),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dense(10,activation='softmax'),
# ])

model = Sequential([
    Reshape((28,28,1), input_shape=(28,28)),
    Conv2D(kernel_size=5, strides=1, filters=16, padding='same', activation='relu', name='layer_conv1'),
    MaxPooling2D(pool_size=2, strides=2),
    Conv2D(kernel_size=5, strides=1, filters=36, padding='same', activation='relu', name='layer_conv2'),
    MaxPooling2D(pool_size=2, strides=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])


model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])
model.summary()

historico = model.fit(x_train, y_train, epochs=10,  validation_freq=1, validation_data=(x_test, y_test))
# Train final
# historico = model.fit(x_train, y_train, epochs=20)

model.save('modelo.h5')

## plots de evolución de loss y accuracy
from matplotlib import pyplot as plt
plt.plot(historico.history['accuracy'])
plt.plot(historico.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
plt.plot(historico.history['loss'])
plt.plot(historico.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()