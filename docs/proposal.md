# Improving "Learning to See in the Dark"

| Name         | Id    | email            |
| ------------ | ----- | ---------------- |
| John Zlotek  | jmz46 | jmz46@drexel.edu |
| Joseph Hines | jth95 | jth95@drexel.edu |

## Relevant Paper

https://cs.nyu.edu/~fergus/papers/zeilerECCV2014.pdf

### Citation

Chen Chen, Qifeng Chen, Jia Xu, and Vladlen Koltun, "Learning to See in the Dark", in CVPR, 2018.

## Existing Implemenation

[https://github.com/cchen156/Learning-to-See-in-the-Dark](https://github.com/cchen156/Learning-to-See-in-the-Dark)

## Abstract

The solution proposed in _Learning to See in the Dark_ is compelling, along
with the implementation linked above. However, the implementation is flawed,
making it difficult for other parties to use. Given that we find the results
compelling, we aim to improve the provided implementation. We are doing this
with the goal of making it easier for more people to use this solution, which
could potentially help improve this implementation. There are high requirements
for both computational power and memory space in order to train the model in
the provided implementation. Our goal is to make the training more memory
efficient so that more people may come along and train their own models.
Along with this, we also aim to develop a basic web application so that users
may upload their own images and see how this solution performs. Ultimately,
our goal is to enable the potential of this solution to truly be explored.

## Requirements

- Improve existing implementation by:
  - `python2` $\rightarrow$ `python3`
  - More extensible code (remove hard coded paths eg. program arguments etc.)
  - Reduce memory overhead (we do not have 64-128GB of RAM available)
    - Use JPEG instead of RAW for inputs (may lower quality of output but makes training easier)
- Possibly contribute to dataset
- Develop small web interface
  - Upload image and recieve corrected image back
