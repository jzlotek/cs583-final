---
title: "Learning to See in the Dark"
author: "Joe Hines and John Zlotek"
---

# Abstract

The purpose of this project was to be able to take the research done by Learning to See in the Dark and make it more accessible and maintainable.
The work done was to port the code over to Python3, remove deprecation warnings due to soon to be outdated code, and create a better code base that is easily readable and therefor more maintainable.

# Introduction

# Related Work

The paper ``Learning to See in the Dark'' proposed a new way of making low light level photography more visible.
Instead of using the traditional pipeline of white balencing, gamma correction, and denoising, the researchers replaced it with a single convolutional neural network trained to do all of the above with better results.
The implementation trained various low light level images with different exposure times and comparing it to a long exposure of the same scene to calulate a loss for that round of training.
Other research has gone into denoiseing and low light enhancement as stated in the paper.
These approaches have limitations unfortunately.


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

We also verified the use of DNG's with the model.
At first, the model only had support verified support for Sony ARW raw files.
From testing it, we were able to verify that DNG raw files work also.
Because of this, phones like the iPhone and Pixel (phones we had on hand) are able to take raw images and input them into the application and get back a corrected image.
This is very useful as phone cameras are notoriously bad at taking images, especially raw, in the dark.
It has gotten better over the years, but from taking outr own photos, we were still seeing a large amount of noise from the images.

# Results
