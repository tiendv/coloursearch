import math
import cv2
import numpy as np
from scipy.ndimage.measurements import label
import collections
from .ColorHistogramExtraction import calc_color_range, extract_rgb_color_histogram


def extract_cumulative_color_histogram(image_location, number_of_color=4096):
    print('Extracting Cumulative Color Histogram for ' + image_location)
    color_range, color, channel_range = calc_color_range(number_of_color)
    number_of_color = len(color)
    rgb_color_histogram = extract_rgb_color_histogram(image_location, color_range, channel_range)

    for key0, value0 in rgb_color_histogram.items():
        for key1, value1 in rgb_color_histogram.items():
            if key1[0][1] < key0[0][0] and key1[1][1] < key0[1][0] and key1[2][1] < key0[2][0]:
                rgb_color_histogram[key0] += value1

    return rgb_color_histogram
