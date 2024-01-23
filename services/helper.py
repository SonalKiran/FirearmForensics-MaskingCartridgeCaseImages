# imports
import cv2
import numpy as np


# helper functions
# function to load an image in grayscale from given path
def load_image_grayscale(im_path, im_size=(150,150)):
    assert type(im_path) == str, "Image path should be a string."
    assert im_path.endswith(('.jpg','jpeg','png')), "Please format the image as a JPEG or PNG file."
    im = cv2.imread(im_path,cv2.IMREAD_GRAYSCALE)
    im = cv2.resize(im, im_size)
    return im


# function to write an image to given path
def write_masked_image(im_path, im):
    assert type(im_path) == str, "Image path should be a string."
    assert im_path.endswith(('.jpg','jpeg','png')), "Please format the image as a JPEG or PNG file."
    im = cv2.imwrite(im_path,im)
    print(f'Successfully saved image! \nPath to saved image: {im_path}')


# function to calculate the distance between two 2-D points
def calculate_distance(pt1, pt2):
    assert isinstance(pt1, (list, tuple)) and isinstance(pt2, (list, tuple)), "Please format points as list - [x,y] or tuple - (x,y)."
    assert len(pt1) == 2 and len(pt2) == 2, "Please provide only the x and y coordinate values for each point."
    assert sum([isinstance(val, (int,float)) for val in pt1]) == 2 == sum([isinstance(val, (int,float)) for val in pt2]), \
        "Please provide the coordinates as integers or floats."
    return np.sqrt(pow(pt1[0] - pt2[0], 2) + pow(pt1[1] - pt2[1], 2))
