# USAGE
# python generate_images_gaussian_noise.py --image AN19111104.png --output transformed_dataset/AN19111104 --dir transformed_dataset/AN19111104_Gaussian
# python generate_images_gaussian_noise.py --image AN19112302.png --output transformed_dataset/AN19112302 --dir transformed_dataset/AN19112302_Gaussian --total 200

# import the necessary packages
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
import numpy as np
import argparse
# import imgaug for adding Gaussian noise
#import imgaug as ia
from imgaug import augmenters as iaa
# import library for list files in directory
from os import listdir
from os.path import isfile, join

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory to store augmentation examples")
ap.add_argument("-d", "--dir", required=True,
	help="path to output directory to store augmentation examples with Gaussian filters")
ap.add_argument("-t", "--total", type=int, default=100,
	help="# of training samples to generate")
args = vars(ap.parse_args())

# load the input image, convert it to a NumPy array, and then
# reshape it to have an extra dimension
print("[INFO] loading example image...")
image = load_img(args["image"])
image = img_to_array(image)
image = np.expand_dims(image, axis=0)

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
imageGen = aug.flow(image, batch_size=1, save_to_dir=args["output"],
	save_prefix="image", save_format="jpg")

# loop over examples from our image data augmentation generator
for image in imageGen:
	# increment our counter
	total += 1

	# if we have reached the specified number of examples, break
	# from the loop
	if total == args["total"]:
		break

# add Gaussian noise and blurring
seq = iaa.Sequential([
	iaa.AdditiveGaussianNoise(scale=(10, 60)), # additive Gaussian noise 
    iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
	], random_order=True) # apply augmenters in random order)

print("[INFO] loading augmented images and generating new images with Gaussian filters...")
filename = [f for f in listdir(args["output"]) if isfile(join(args["output"], f))]
for i in filename:
	if i.endswith(".jpg"):
		image_aug = load_img(args["output"] + '/' + i)
		image_aug = img_to_array(image_aug)
		image_aug_seq = seq(image=image_aug)
		image_aug_seq = np.expand_dims(image_aug_seq, axis=0)
		# construct the image generator for data augmentation then
		# initialize the total number of images generated thus far
		no_aug = ImageDataGenerator(zoom_range=0)
		total = 0
		# construct the actual Python generator
		imageGen = no_aug.flow(image_aug_seq, batch_size=1, save_to_dir=args["dir"],
			save_prefix="image", save_format="jpg")
		# loop over examples from our image data augmentation generator
		for image in imageGen:
			# increment our counter
			total += 1

			# if we have reached the specified number of examples, break
			# from the loop
			if total == 1:#args["total"]:
				break
