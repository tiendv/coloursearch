import cv2
import time
import numpy as np
import collections
from ..constants import *
from ..utilities.Utilities import *
from .ColorHistogramExtraction import calc_color_range
from ..models.ColorCorrelogram import ColorCorrelogram


def extract_color_correlogram(img_extraction_id, image_location, number_of_colors=64, d=7, increment=1):
    print('Extracting Color Correlogram for ' + image_location)
    D = []
    if d is None or d < 1:
        D = [1, 3, 5, 7]
    else:
        i = 1
        while i < d:
            D.append(int(i))
            i += increment

    color_ranges, colors, channel_ranges = calc_color_range(number_of_colors)
    pair_of_ranges = []

    for color_range in color_ranges:
        pair_of_ranges.append([[color_range[0][0], color_range[1][0], color_range[2][0]],
                               [color_range[0][1], color_range[1][1], color_range[2][1]]])
    number_of_colors = len(colors)
    m = number_of_colors

    img = cv2.imread(image_location)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width = img.shape[:2]
    start_time = time.time()
    if width > MAX_IMAGE_WIDTH:
        img = image_resize(img, width=MAX_IMAGE_WIDTH)
        height, width = img.shape[:2]
        if height > MAX_IMAGE_HEIGHT:
            img = image_resize(img, height=MAX_IMAGE_HEIGHT)
    elif height > MAX_IMAGE_HEIGHT:
        img = image_resize(img, height=MAX_IMAGE_HEIGHT)
        height, width = img.shape[:2]
        if width > MAX_IMAGE_WIDTH:
            img = image_resize(img, width=MAX_IMAGE_WIDTH)
    print('Resize to {}x{}'.format(img.shape[0], img.shape[1]))
    print("--- Resize: %s seconds ---" % (time.time() - start_time))

    img = np.float32(img)

    histogram = collections.OrderedDict()
    color_pixels = collections.OrderedDict()

    for c in color_ranges:
        histogram[c] = 0
        color_pixels[c] = []

    start_time = time.time()

    for pair_of_range in pair_of_ranges:
        lower = np.array(pair_of_range[0])  # BGR-code of your lowest red
        upper = np.array(pair_of_range[1])  # BGR-code of your highest red
        mask = cv2.inRange(img, lower, upper)
        color_range = ((pair_of_range[0][0], pair_of_range[1][0]),
                       (pair_of_range[0][1], pair_of_range[1][1]),
                       (pair_of_range[0][2], pair_of_range[1][2]))
        # get all non zero values
        coord = cv2.findNonZero(mask)
        if coord is not None:
            for item in coord:
                color_pixels[color_range].append([item[0][0], item[0][1]])
            histogram[color_range] = len(coord)
        else:
            histogram[color_range] = 0

    # for i in range(0, len(img)):
    #     for j in range(0, len(img[i])):
    #         channel_0 = None
    #         channel_1 = None
    #         channel_2 = None
    #         for cr in channel_ranges:
    #             if cr[0] <= img[i][j][0] <= cr[1]:
    #                 channel_0 = cr
    #             if cr[0] <= img[i][j][1] <= cr[1]:
    #                 channel_1 = cr
    #             if cr[0] <= img[i][j][2] <= cr[1]:
    #                 channel_2 = cr
    #             if channel_0 is not None and channel_1 is not None and channel_2 is not None:
    #                 break
    #         histogram[(channel_0, channel_1, channel_2)] += 1
    #         color_pixels[(channel_0, channel_1, channel_2)].append([i, j])
    print("--- %s seconds ---" % (time.time() - start_time))

    epsilon = 10
    gamma = {k: {} for k in D}
    if D[len(D) - 1] < epsilon:
        for k in D:
            for color_range in color_ranges:
                pixels = color_pixels[color_range]
                if histogram[color_range] != 0:
                    gamma[k][color_range] = calc_gamma(k, pixels) / (histogram[color_range] * 8 * k)
                else:
                    gamma[k][color_range] = 0.0

    print(gamma)

    k = None
    for key, value in gamma.items():
        k = key
        for key1, value1 in value.items():
            instance = ColorCorrelogram(image_extraction_id=img_extraction_id)
            instance.k = k
            instance.ccomponent1_min = key1[0][0]
            instance.ccomponent1_max = key1[0][1]
            instance.ccomponent2_min = key1[1][0]
            instance.ccomponent2_max = key1[1][1]
            instance.ccomponent3_min = key1[2][0]
            instance.ccomponent3_max = key1[2][1]
            instance.value = value1
            instance.save()
            print('Saved k = ' + str(k) + ', ' + str(key1) + ': ' + str(value1))
    return gamma


def calc_gamma(k, pixels):
    print('calculating gamma for k = ' + str(k))
    lambda_h1 = lambda_h2 = lambda_v1 = lambda_v2 = 0
    temp_pixels = set(tuple(i) for i in pixels)
    for pixel in pixels:
        for i in range(0, 2 * k):
            if (pixel[0] - k + i, pixel[1] + k) in temp_pixels:
                lambda_h1 += 1
            if (pixel[0] - k + i, pixel[1] - k) in temp_pixels:
                lambda_h2 += 1

        for j in range(0, 2 * k - 2):
            if (pixel[0] - k, pixel[1] - k + 1 + j) in temp_pixels:
                lambda_v1 += 1
            if (pixel[0] + k, pixel[1] - k + 1 + j) in temp_pixels:
                lambda_v2 += 1
    return lambda_h1 + lambda_h2 + lambda_v1 + lambda_v2
