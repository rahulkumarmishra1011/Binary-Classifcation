# -*- coding: utf-8 -*-
"""Untitled44.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Lqtn6Wg43WV6woldVaN-GMbpBiOTrrC
"""

import zipfile

# Download zip file of pizza_steak images
zip_ref = "https://huggingface.co/datasets/rahulmishra/pizza_steak/resolve/main/pizza_steak.zip"

# Unzip the downloaded file
zip_ref = zipfile.ZipFile("pizza_steak.zip", "r")
zip_ref.extractall()
zip_ref.close()

import os

# Walk through pizza_steak directory and list number of files
for dirpath, dirnames, filenames in os.walk("pizza_steak"):
  print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'.")

# Get the class names (programmatically, this is much more helpful with a longer list of classes)
import pathlib
import numpy as np
data_dir = pathlib.Path("pizza_steak/train/") # turn our training path into a Python path
class_names = np.array(sorted([item.name for item in data_dir.glob('*')])) # created a list of class_names from the subdirectories
print(class_names)

# View an image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_random_image(target_dir, target_class):
  # Setup target directory (we'll view images from here)
  target_folder = target_dir+target_class

  # Get a random image path
  random_image = random.sample(os.listdir(target_folder), 1)
    


  # Read in the image and plot it using matplotlib
  img = mpimg.imread(target_folder + "/" + random_image[0])
  plt.imshow(img)
  plt.title(target_class)
  plt.axis("off");

  print(f"Image shape: {img.shape}") # show the shape of the image

  return img

# View a random image from the training dataset
img = view_random_image(target_dir="pizza_steak/train/",target_class="steak")

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define training and test directory paths
train_dir = "pizza_steak/train/"
test_dir = "pizza_steak/test/"

# Plot the validation and training data separately
def plot_loss_curves(history):
  """
  Returns separate loss curves for training and validation metrics.
  """ 
  loss = history.history['loss']
  val_loss = history.history['val_loss']

  accuracy = history.history['accuracy']
  val_accuracy = history.history['val_accuracy']

  epochs = range(len(history.history['loss']))

  # Plot loss
  plt.plot(epochs, loss, label='training_loss')
  plt.plot(epochs, val_loss, label='val_loss')
  plt.title('Loss')
  plt.xlabel('Epochs')
  plt.legend()

  # Plot accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label='training_accuracy')
  plt.plot(epochs, val_accuracy, label='val_accuracy')
  plt.title('Accuracy')
  plt.xlabel('Epochs')
  plt.legend();

# Create ImageDataGenerator training instance with data augmentation
train_datagen_augmented = ImageDataGenerator(rescale=1/255.,
                                             rotation_range=20, # rotate the image slightly between 0 and 20 degrees (note: this is an int not a float)
                                             shear_range=0.2, # shear the image
                                             zoom_range=0.2, # zoom into the image
                                             width_shift_range=0.2, # shift the image width ways
                                             height_shift_range=0.2, # shift the image height ways
                                             horizontal_flip=True) # flip the image on the horizontal axis

# Create ImageDataGenerator training instance without data augmentation
train_datagen = ImageDataGenerator(rescale=1/255.) 

# Create ImageDataGenerator test instance without data augmentation
test_datagen = ImageDataGenerator(rescale=1/255.)

# Import data and augment it from training directory
print("Augmented training images:")
train_data_augmented = train_datagen_augmented.flow_from_directory(train_dir,
                                                                   target_size=(224, 224),
                                                                   batch_size=32,
                                                                   class_mode='binary',
                                                                   shuffle=False) # Don't shuffle for demonstration purposes, usually a good thing to shuffle

# Create non-augmented data batches
print("Non-augmented training images:")
train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=(224, 224),
                                               batch_size=32,
                                               class_mode='binary',
                                               shuffle=False) # Don't shuffle for demonstration purposes

print("Unchanged test images:")
test_data = test_datagen.flow_from_directory(test_dir,
                                             target_size=(224, 224),
                                             batch_size=32,
                                             class_mode='binary')

# Import data and augment it from directories
train_data_augmented_shuffled = train_datagen_augmented.flow_from_directory(train_dir,
                                                                            target_size=(224, 224),
                                                                            batch_size=32,
                                                                            class_mode='binary',
                                                                            shuffle=True)

# Make the creating of our model a little easier
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Activation
from tensorflow.keras import Sequential

# Create a CNN model (same as Tiny VGG but for binary classification - https://poloclub.github.io/cnn-explainer/ )
model_8 = Sequential([
  Conv2D(10, 3, activation='relu', input_shape=(224, 224, 3)), # same input shape as our images
  Conv2D(10, 3, activation='relu'),
  MaxPool2D(),
  Conv2D(10, 3, activation='relu'),
  Conv2D(10, 3, activation='relu'),
  MaxPool2D(),
  Flatten(),
  Dense(1, activation='sigmoid')
])

# Compile the model
model_8.compile(loss="binary_crossentropy",
                optimizer=tf.keras.optimizers.Adam(),
                metrics=["accuracy"])

# Fit the model
history_8 = model_8.fit(train_data_augmented_shuffled,
                        epochs=30,
                        steps_per_epoch=len(train_data_augmented_shuffled),
                        validation_data=test_data,
                        validation_steps=len(test_data))

"""# Making a prediction with our trained model"""

# Classes we're working with
print(class_names)

# View our example image
# wget https://github.com/mrdbourke/tensorflow-deep-learning/blob/ff0a93f68915e85bcb509a0c636d16f4567fbf8a/images/03-steak.jpeg
# steak = mpimg.imread("03-steak.jpeg")
# plt.imshow(steak)
# plt.axis(False);

# Check the shape of our image
#steak.shape

# Add an extra axis
#print(f"Shape before new dimension: {steak.shape}")
#steak = tf.expand_dims(steak, axis=0) # add an extra dimension at axis 0
#steak = steak[tf.newaxis, ...] # alternative to the above, '...' is short for 'every other dimension'
#print(f"Shape after new dimension: {steak.shape}")
#steak

# Make a prediction on custom image tensor
#pred = model_8.predict(steak)
#pred

# Load in and preprocess our custom image
#steak = pred_and_plot("03-steak.jpeg")
#steak

# Create a function to import an image and resize it to be able to be used with our model
def load_and_prep_image(filename, img_shape=224):
  """
  Reads an image from filename, turns it into a tensor
  and reshapes it to (img_shape, img_shape, colour_channel).
  """
  # Read in target file (an image)
  #img = tf.io.read_file(filename)
  #print(img)
  # Decode the read file into a tensor & ensure 3 colour channels 
  # (our model is trained on images with 3 colour channels and sometimes images have 4 colour channels)
  img = filename
  #img = tf.image.decode_image(img, channels=3)
  
  # Resize the image (to the same size our model was trained on)
  img = tf.image.resize(img, size = [img_shape, img_shape])
  print(img.shape)
  # Rescale the image (get all values between 0 and 1)
  img = img/255.
  return img

def pred_and_plot(filename):
  """
  Imports an image located at filename, makes a prediction on it with
  a trained model and plots the image with the predicted class as the title.
  """
  # Import the target image and preprocess it
  # print(filename.shape)
  img = load_and_prep_image(filename)
  
  # Make a prediction
  pred = model_8.predict(tf.expand_dims(img, axis=0))
  class_names = ['Pizza🍕','Steak🥩']
  # Get the predicted class
  pred_class = class_names[int(tf.round(pred)[0][0])]
  return pred_class
  # Plot the image and predicted class
 # plt.imshow(img)
  #plt.title(f"Prediction: {pred_class}")
  #plt.axis(False);

# Test our model on a custom image
#pred_and_plot("03-steak.jpeg")

#import cv2
#val = cv2.imread("03-steak.jpeg")
#val.shape

from pathlib import Path
# Create a list of example inputs to our Gradio demo
test_data_paths = list(Path(test_dir).glob("*/*.jpg"))

example_list = [[str(filepath)] for filepath in random.sample(test_data_paths, k=3)]
example_list

# Import/install Gradio 
import gradio as gr
    
print(f"Gradio version: {gr.__version__}")

import gradio as gr

# Create title, description and article strings
title = "FoodVision Mini 🥩🍕"
description = "A CNN model to classify images of food as pizza or steak ."


# Create the Gradio demo
demo = gr.Interface(fn=pred_and_plot, # mapping function from input to output
                    inputs=["image"], # what are the inputs?
                    outputs=["text"], # our fn has two outputs, therefore we have two outputs
                    examples=example_list, 
                    title=title,
                    description=description)

# Launch the demo!
demo.launch(inline=True) # generate a publically shareable URL?

