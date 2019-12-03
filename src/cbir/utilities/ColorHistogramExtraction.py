import math
import numpy as np
import cv2
import logging

logger = logging.getLogger(__name__)


def calc_color_range(number_of_color):
    number_of_range_per_channel = number_of_color**(1/3)
    if (math.ceil(number_of_range_per_channel) - number_of_range_per_channel) < 0.001:
        number_of_range_per_channel = math.ceil(number_of_range_per_channel)
    else:
        number_of_range_per_channel = int(number_of_range_per_channel)
    print('number_of_range_per_channel: ' + str(number_of_range_per_channel))

    # Value with distance
    color = []
    color_range = []
    value = []
    value_range = []
    distance = round(1.0 * 255 / number_of_range_per_channel)

    for i in range(0, number_of_range_per_channel):
        if i != 0:
            start = distance * i + 1
        else:
            start = 0
        if i != (number_of_range_per_channel - 1):
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


def extract_rgb_color_histogram(image_location, coarse_color_range, coarse_channel_range):
    img = cv2.imread(image_location)
    img = img.reshape((-1, 3))
    img = np.float32(img)

    histogram = {}

    for color_range in coarse_color_range:
        histogram[color_range] = 0

    for pixel in img:
        channel_0 = None
        channel_1 = None
        channel_2 = None
        for channel_range in coarse_channel_range:
            if channel_range[0] <= pixel[0] <= channel_range[1]:
                channel_0 = channel_range
            if channel_range[0] <= pixel[1] <= channel_range[1]:
                channel_1 = channel_range
            if channel_range[0] <= pixel[2] <= channel_range[1]:
                channel_2 = channel_range
            if channel_0 is not None and channel_1 is not None and channel_2 is not None:
                break
        histogram[(channel_0, channel_1, channel_2)] += 1

    return histogram


