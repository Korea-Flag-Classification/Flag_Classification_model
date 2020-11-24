from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import keras
from keras import layers
import os
from keras.models import load_model
from keras.callbacks import EarlyStopping

os.environ['KMP_DUPLICATE_LIB_OK']='True'

train = ImageDataGenerator(rescale = 1/255)
val =ImageDataGenerator(rescale=1/255)

train_dataset = train.flow_from_directory('/Users/jeongjaeyeong/Desktop/gitgit/Vegita/wrong or right/train/',
                                          target_size = (200,200),
                                          batch_size = 32,
                                          shuffle=True,
                                          class_mode='binary')

val_dataset = train.flow_from_directory('/Users/jeongjaeyeong/Desktop/gitgit/Vegita/wrong or right/val/',
                                          target_size = (200,200),
                                          batch_size = 32,
                                          shuffle=True,
                                          class_mode='binary')



xception= keras.applications.Xception(weights='imagenet',include_top=False, input_shape=(200,200,3))

x = xception.output

flatten_layer = layers.Flatten()  # instantiate the layer
x = flatten_layer(x)

x = layers.Dense(512)(x)
x = layers.BatchNormalization()(x)
prediction = layers.Dense(1, activation='sigmoid')(x)

model =keras.Model(xception.input, prediction)

model.compile(loss= keras.losses.BinaryCrossentropy() , optimizer= keras.optimizers.RMSprop(lr=0.001), metrics=['accuracy'])

model_fit = model.fit(train_dataset,
                      steps_per_epoch = 2,
                      epochs= 50,
                      callbacks= [EarlyStopping(monitor='loss',patience=5)],
                      validation_data = val_dataset)

model.save('xception.h5')