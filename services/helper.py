# imports
import cv2

# import numpy as np
import math
from typing import Any, Union, Sequence
import numpy.typing as npt


# helper functions
# function to load an image in grayscale from given path
def load_image_grayscale(im_path: str, im_size: tuple[int, int] = (150, 150)) -> npt.NDArray[Any]:
    if not isinstance(im_path, str):
        raise TypeError("Image path should be a string")
    if not im_path.endswith((".jpg", ".jpeg", ".png")):
        raise TypeError(
            f"This file type is not supported.\nExtension must be one of - [.jpeg, .jpg, .png]. Instead got a file ending with {'.' + im_path.split('.')[-1]}."
        )
    im = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)
    im = cv2.resize(im, im_size)
    return im


# function to write an image to given path
def write_masked_image(im_path: str, im: npt.NDArray[Any]) -> None:
    if not isinstance(im_path, str):
        raise TypeError("Image path should be a string")
    if not im_path.endswith((".jpg", ".jpeg", ".png")):
        raise TypeError(
            f"This file type is not supported.\nExtension must be one of - [.jpeg, .jpg, .png]. Instead got a file ending with {'.' + im_path.split('.')[-1]}."
        )
    cv2.imwrite(im_path, im)
    print(f"Successfully saved image!\nPath to saved image: {im_path}")


# function to calculate the distance between two 2-D points
Num = Union[int, float]


def calculate_distance(pt1: Sequence[Num], pt2: Sequence[Num]) -> float:
    if not isinstance(pt1, (list, tuple)) and not isinstance(pt2, (list, tuple)):
        raise TypeError("Please format points as list - [x,y] or tuple - (x,y).")
    if not (len(pt1) == 2 and len(pt2) == 2):
        raise AssertionError("Please provide only the x and y coordinates for each point.")
    if not (
        sum([isinstance(val, (int, float)) for val in pt1])
        == 2
        == sum([isinstance(val, (int, float)) for val in pt2])
    ):
        raise TypeError("Please provide the coordinates as integers or floats.")
    return math.sqrt(pow(pt1[0] - pt2[0], 2) + pow(pt1[1] - pt2[1], 2))
