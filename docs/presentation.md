---
title: 'Learning to See in the Dark'
subtitle: 'Improving Accessibility'
author: Joseph Hines and John Zlotek
date: \today
---

\pagebreak

# Paper Overview

## Goal and Approach

- High ISO is noisy

* Get long exposure quality with short exposures

- Train a model to reflect this

## Their Results

![](./pics/1.png)

## Their Results

![](./pics/2.png)

# Flaws of Current Implementation

## Python2

- Support ending soon

* Rife with deprecation warnings

- Can hurt adoption

## Provided Data/Models

- Unrealistic Hardware requirements to train

* Code is disjoint, tricky to get started

- Restricted to two Camera brands/RAW formats

# Demo

## Web App

- Increase exposure

* Encourage curiosity

# Our Results/Improvements

## Results

![](./pics/example_1.png)

##

![](./pics/example_2.png)

##

![](./pics/example_3.png)

## Ground Truth

![](./pics/example_4_gt.png)

## Traditional Scaling

![](./pics/example_4_scale.png)

## Our Model

![](./pics/example_4_out.png)

## Ground Truth

![](./pics/example_5_gt.png)

## Traditional Scaling

![](./pics/example_5_scale.png)

## Our Model

![](./pics/example_5_out.png)

## Contributions

- Implement batching to reduce training memory usage

* Support DNG (Smartphone RAW)

- Created a Web App

* Basic CLI + module

- Refactored shared code

* Created a IPython Notebook for Colab

## Going Forward

- Supporting more raw formats

* General JPG/PNG implementation

- Visualize the model

* Optimize the amplification parameter

- Better hosting solution for dataset

* Put it in an App and charge \$5

# Thank you!


