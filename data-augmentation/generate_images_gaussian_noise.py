# USAGE
# python generate_images_gaussian_noise.py --image AN19111104.png --output transformed_dataset/AN19111104
# python generate_images_gaussian_noise.py --image AN19112302.png --output transformed_dataset/AN19112302 --total 200

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse
# import imgaug for adding Gaussian noise
import imgaug as ia
from imgaug import augmenters as iaa

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory to store augmentation examples")
ap.add_argument("-t", "--total", type=int, default=100,
	help="# of training samples to generate")
args = vars(ap.parse_args())

# load the input image, convert it to a NumPy array, and then
# reshape it to have an extra dimension
print("[INFO] loading example image...")
image = load_img(args["image"])
image = img_to_array(image)
# use imgaug package to add Gaussian noise
ia.seed(4)
AGN = iaa.AdditiveGaussianNoise(scale=(10, 60))
image_aug = AGN(image=image)
# expand dimensions for Keras
image_aug = np.expand_dims(image_aug, axis=0)

# construct the image generator for data augmentation then
# initialize the total number of images generated thus far
aug = ImageDataGenerator(
	rotation_range=20, # lower to 20
	zoom_range=0, # lower to 0
	width_shift_range=0.1, # keep low
	height_shift_range=0.1, # keep low
	shear_range=0.30, # increase
	horizontal_flip=True,
	brightness_range=(0.8,0.1),
	fill_mode="reflect") # reflect
total = 0

# construct the actual Python generator
print("[INFO] generating images...")
imageGen = aug.flow(image_aug, batch_size=1, save_to_dir=args["output"],
	save_prefix="image", save_format="jpg")

# loop over examples from our image data augmentation generator
for image in imageGen:
	# increment our counter
	total += 1

	# if we have reached the specified number of examples, break
	# from the loop
	if total == args["total"]:
		break