# Visualizing a Deep Neural Net Classifier

> Joseph Hines and John Zlotek

| Name         | Id    | email            |
| ------------ | ----- | ---------------- |
| John Zlotek  | jmz46 | jmz46@drexel.edu |
| Joseph Hines | jth95 | jth95@drexel.edu |

## Relevant Paper

https://cs.nyu.edu/~fergus/papers/zeilerECCV2014.pdf

## Citation

Chen Chen, Qifeng Chen, Jia Xu, and Vladlen Koltun, "Learning to See in the Dark", in CVPR, 2018.

## Existing Implemenation

![https://github.com/cchen156/Learning-to-See-in-the-Dark](https://github.com/cchen156/Learning-to-See-in-the-Dark)

## Abstract

Our goal is to create a version of this implemenation that does is not as resource intensive so that people with lower end systems can test and run this code without having to rent a compute unit.
Along with this we plan to develop a web application so that people can use the model in an intuitve way.
The short commings of this implemenation is that for one, it is dependent on having access to a very highly spec'd computer.
Along with this, you need knowledge of running python code natively with tensorflow.

## Requirements

- Improve existing implementation by:
  - `python2` \rightarrow `python3`
  - More extensible code (remove hard coded paths eg. program arguments etc.)
  - Reduce memory overhead (we do not have 64-128GB of RAM available)
    - Use JPEG instead of RAW for inputs (may lower quality of output but makes training easier)
- Possibly contribute to dataset
- Develop small web interface
  - Upload image and recieve corrected image back
