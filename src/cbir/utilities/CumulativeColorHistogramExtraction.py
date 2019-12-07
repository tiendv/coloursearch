import math
import cv2
import numpy as np
from scipy.ndimage.measurements import label
import collections
from .ColorHistogramExtraction import calc_color_range, extract_rgb_color_histogram
from ..models.CumulativeColorHistogram import CumulativeColorHistogram


def extract_cumulative_color_histogram(img_extraction_id, image_location, number_of_color=4096):
    print('Extracting Cumulative Color Histogram for ' + image_location)
    color_range, color, channel_range = calc_color_range(number_of_color)
    number_of_color = len(color)
    rgb_color_histogram = extract_rgb_color_histogram(image_location, color_range, channel_range)

    for key0, value0 in rgb_color_histogram.items():
        for key1, value1 in rgb_color_histogram.items():
            if key1[0][1] < key0[0][0] and key1[1][1] < key0[1][0] and key1[2][1] < key0[2][0]:
                rgb_color_histogram[key0] += value1

    for key, value in rgb_color_histogram.items():
        instance = CumulativeColorHistogram()
        instance.image_extraction_id = img_extraction_id
        instance.ccomponent1_min = key[0][0]
        instance.ccomponent1_max = key[0][1]
        instance.ccomponent2_min = key[1][0]
        instance.ccomponent2_max = key[1][1]
        instance.ccomponent3_min = key[2][0]
        instance.ccomponent3_max = key[2][1]
        instance.value = value
        instance.save()

    return rgb_color_histogram
