import math
import numpy as np
import cv2
import collections
import logging

from ..models import ColorHistogram, Extraction

logger = logging.getLogger(__name__)


def calc_color_range(number_of_colors):
    number_of_ranges_per_channel = number_of_colors**(1/3)
    if (math.ceil(number_of_ranges_per_channel) - number_of_ranges_per_channel) < 0.001:
        number_of_ranges_per_channel = math.ceil(number_of_ranges_per_channel)
    else:
        number_of_ranges_per_channel = int(number_of_ranges_per_channel)
    print('number_of_ranges_per_channel: ' + str(number_of_ranges_per_channel))

    # Value with distance
    color = []
    color_range = []
    value = []
    value_range = []
    distance = round(1.0 * 255 / number_of_ranges_per_channel)

    for i in range(0, number_of_ranges_per_channel):
        if i != 0:
            start = distance * i + 1
        else:
            start = 0
        if i != (number_of_ranges_per_channel - 1):
            end = distance * (i + 1)
        else:
            end = 255
        average = int((start + end) / 2)
        value.append(average)
        value_range.append((start, end))

    for i in range(0, len(value_range)):
        for j in range(0, len(value_range)):
            for k in range(0, len(value_range)):
                color_range.append((value_range[i], value_range[j], value_range[k]))
                color.append((value[i], value[j], value[k]))

    return color_range, color, value_range


def extract_rgb_color_histogram(image_location, color_range, channel_range):
    if type(image_location) == str:
        img = cv2.imread(image_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape((-1, 3))
        img = np.float32(img)
    elif type(image_location) == list:
        image_location = np.array(image_location)
        image_location = cv2.cvtColor(image_location, cv2.COLOR_BGR2RGB)
        img = []
        for row in image_location:
            for pixel in row:
                img.append(pixel)

    number_of_pixels = len(img)

    histogram = collections.OrderedDict()

    for c in color_range:
        histogram[c] = 0

    for pixel in img:
        channel_0 = None
        channel_1 = None
        channel_2 = None
        for cr in channel_range:
            if cr[0] <= pixel[0] <= cr[1]:
                channel_0 = cr
            if cr[0] <= pixel[1] <= cr[1]:
                channel_1 = cr
            if cr[0] <= pixel[2] <= cr[1]:
                channel_2 = cr
            if channel_0 is not None and channel_1 is not None and channel_2 is not None:
                break
        histogram[(channel_0, channel_1, channel_2)] += 1

    for key, value in histogram.items():
        histogram[key] = value / number_of_pixels

    return histogram


def extract_cielab_color_histogram(image_location, color_range, channel_range):
    if type(image_location) == str:
        img = cv2.imread(image_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        img = img.reshape((-1, 3))
        img = np.float32(img)
    elif type(image_location) == list:
        image_location = np.array(image_location)
        image_location = image_location.astype(np.uint8)
        image_location = cv2.cvtColor(image_location, cv2.COLOR_BGR2Lab)
        print(image_location)
        img = []
        for row in image_location:
            for pixel in row:
                img.append(pixel)

    number_of_pixels = len(img)

    histogram = collections.OrderedDict()

    for c in color_range:
        histogram[c] = 0

    for pixel in img:
        channel_0 = None
        channel_1 = None
        channel_2 = None
        for cr in channel_range:
            if cr[0] <= pixel[0] <= cr[1]:
                channel_0 = cr
            if cr[0] <= pixel[1] <= cr[1]:
                channel_1 = cr
            if cr[0] <= pixel[2] <= cr[1]:
                channel_2 = cr
            if channel_0 is not None and channel_1 is not None and channel_2 is not None:
                break
        histogram[(channel_0, channel_1, channel_2)] += 1

    for key, value in histogram.items():
        histogram[key] = value / number_of_pixels

    return histogram

