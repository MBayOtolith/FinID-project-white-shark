# data-augmentation
TensorFlow backened, Keras ImageDataGenerator, dataset generation

## Introduction
In Shark Fin ID project at Monterey Bay Aquarium, we have archived fin images for 500 individual sharks. However, 60% of these individual sharks archived in our dataset have less than 10 clear fin images. One way to train a robust shark fin recognition deep learning system and to increase the generalizability of the model is to expand the fin dataset by data augmentation technique. 

In this technique, we obtain augmented data from the original fin images by applying simple geometric transforms, such as random translations, rotations, changes in scale, shearing, horizontal and vertical flips. Applying transformations to an input image will change its appearance slightly, but it does not change the class label — thereby making data augmentation a very natural and easy method to apply for computer vision tasks.

This repository contains the script for generating randomly transformed shark fin images using Keras ImageDataGenerator. The main script is generic; you can use it to augment any kind of images.

## Directory structure
Below is the directory structure; here we have 2 shark fin examples (`AN19111104.png` and `AN19112302.png`):

```
    ├── generate_images.py         <- main script
    ├── AN19111104.png             <- shark fin image example 1
    ├── AN19112302.png             <- shark fin image example 1
    ├── transformed_dataset        <- transformed dataset folder
          ├── AN19111104           <- for storing newly transformed shark fin images
          ├── AN19112302           <- for storing newly transformed shark fin images
          ├── AN19111104_Gaussian  <- for storing newly transformed shark fin images (plus Gaussian filters)
          ├── AN19112302_Gaussian  <- for storing newly transformed shark fin images (plus Gaussian filters)
```
Note that the `transformed_dataset` folder is empty. You will use the main script `generate_images.py` to generate transformed images into your directory.

## Code
The script `generate_images.py` is in Python, using Keras ImageDataGenerator (see Keras [documentation](https://keras.io/preprocessing/image/) for more details.) to generate transformed images. 

You will parse 3 command line arguments to run the code:
- `--image`: The path to the input image. You will generate additional random, transformed versions of this image.
- `--output`: The path to the output directory to store the data augmentation examples. Here we use `transformed_dataset/AN19111104` or `transformed_dataset/AN19112302`.
- `--total`: The number of sample images to generate. Default is 100 images.

## Run
Examples:
- `python generate_images.py --image AN19111104.png --output transformed_dataset/AN19111104` (default: 100 images)
- `python generate_images.py --image AN19112302.png --output transformed_dataset/AN19112302 --total 200` (specify to generate 200 images)

## Transformation arguments
In the main script `generate_images.py`, starting `L31` where you can adjust the transformation parameters, such as the degrees of rotations, scale, shearing, horizontal and vertical flips. See `ImageDataGenerator class` in Keras [documentation](https://keras.io/preprocessing/image/) for more details.

## [Advanced functionality] Adding Gaussian noise
Here we use [imgaug](https://github.com/aleju/imgaug) package for adding Gaussian noise/ blurring layer. Install with pip: `pip install imgaug`; install with Anaconda: `conda config --add channels conda-forge`, then `conda install imgaug`. To adjust parameters, refer to `L67` and `L68`in `generat_images_gaussian_noise.py` for additive Gaussian noise and Gaussian blurring, respectively. The script will add either additive Gaussian noise or Gaussian blurring (randomly select) to the augmented images and store in another directory (that you have to specify with `--dir`). To run:

- `python generate_images_gaussian_noise.py --image AN19111104.png --output transformed_dataset/AN19111104 --dir transformed_dataset/AN19111104_Gaussian` (default: 100 images)
- `python generate_images_gaussian_noise.py --image AN19112302.png --output transformed_dataset/AN19112302 --dir transformed_dataset/AN19112302_Gaussian --total 200` (specify to generate 200 images)

## Requirements
- [Anaconda / Python 3.6](https://www.continuum.io/downloads)
- [TensorFlow 1.12](https://www.tensorflow.org/)
- [Keras 2.2](https://keras.io/)
- [imgaug](https://github.com/aleju/imgaug)

## Contact
zacycliu@stanford.edu

## Last updated
March 3, 2020



