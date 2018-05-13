#vivekyadavofficial
#import required modules
from keras.layers import GlobalAveragePooling2D, Input, Conv2D, MaxPooling2D, multiply, Flatten, Dense, concatenate
from keras.models import Model
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.optimizers import SGD

#load cifar10 datset
(x_train, y_train),(x_test,y_test) = cifar10.load_data()

#normalize data
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train = x_train / 255.0
x_test = x_test / 255.0

#convert categorical variable to one-hot encoded matrix
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

#define input format
input_image = Input(shape = (32, 32, 3))

#define squeeze and excitation block
def se_block(cnn_input, ratio=16):
    x = GlobalAveragePooling2D()(cnn_input)
    channel = cnn_input._keras_shape[-1]
    x = Dense(channel//ratio, activation='relu')(x)
    x = Dense(channel, activation='sigmoid')(x)
    return multiply([cnn_input, x])

#define inception network architecture
incep_in1 = Conv2D(64, (1,1), padding='same', activation='relu')(input_image)

incep_in1 = Conv2D(64, (3,3), padding='same', activation='relu')(incep_in1)

incep_in2 = Conv2D(64, (1,1), padding='same', activation='relu')(input_image)

incep_in2 = Conv2D(64, (5,5), padding='same', activation='relu')(incep_in2)

incep_in3 = MaxPooling2D((3,3), strides=(1,1), padding='same')(input_image)

incep_in3 = Conv2D(64, (1,1), padding='same', activation='relu')(incep_in3)

#combining inception layers to form inception module
output_inception = concatenate([incep_in1,	 incep_in2, incep_in3], axis=3)

#integrate se_block with inception module
se_out = se_block(output_inception)

#add last output layer to give categorical output for classification
output = Flatten()(se_out)
out = Dense(10, activation='softmax')(output)

model = Model(input=input_image, outputs=out)


#summarise the model
print(model.summary())


#compile model with Adam Optimizer
epochs = 20
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)

model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=epochs, batch_size=32)

acc = model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (acc[1]*100))
