# Abstract

The purpose of this project was to be able to take the research done by Learning to See in the Dark and make it more accessible and maintainable.
The work done was to port the code over to Python3, remove deprecation warnings due to soon to be outdated code, and create a better codebase that is easily readable and therefor more maintainable.

# Introduction

# Related Work

# Contributions

We were able to port over most of the existing code to Python3 and started using Keras with the tensorflow back end instead of just tensorflow alone.
This allows the code to last further into the future without the need to change the code to keep up to date with newer package versions in theory.
The original implementation required anywhere from 64 to 128 GB of ram to run the training set.
The research paper's implementation loaded all images into ram if not loaded in order to lower the read times from disk as the files are anywhere from 10 to 20+ MB each.
This was not acceptable to be able to run on any normal system which has anywhere from 8 to 16 GB of ram on average.
This change does slightly increase training times, but it can most likely be run on any system with any normal amount of ram as opposed to 128 GB in the worst case.
In our case, it helped while training as we only had 12 GB of ram on a Google Colaboratory virtual machine.
This allowed us to train and test using Keras as our machine learning implementation of choice.

We have also created a web application to allow people with minimal coding or machine learning experience to see what would happen if they run the network on their own raw images.
The web application uses a Python3 flask back end for taking in the POST requests and forwarding the images to the Keras neural network for processing.
It will then send back a zipfile that contains all of the processed images in png format.

# Results
