import cv2
import numpy as np
import collections
from .ColorHistogramExtraction import calc_color_range


def extract_color_correlogram(image_location, number_of_color=64, d=7, increment=1):
    print('Extracting Color Correlogram for ' + image_location)
    D = []
    if d is None or d < 1:
        D = [1, 3, 5, 7]
    else:
        i = 1
        while i < d:
            D.append(i)
            i += increment

    color_ranges, colors, channel_ranges = calc_color_range(number_of_color)
    number_of_color = len(colors)
    m = number_of_color

    img = cv2.imread(image_location)
    img = np.float32(img)

    histogram = collections.OrderedDict()
    color_pixels = collections.OrderedDict()

    for c in color_ranges:
        histogram[c] = 0
        color_pixels[c] = []

    for i in range(0, len(img)):
        for j in range(0, len(img[i])):
            channel_0 = None
            channel_1 = None
            channel_2 = None
            for cr in channel_ranges:
                if cr[0] <= img[i][j][0] <= cr[1]:
                    channel_0 = cr
                if cr[0] <= img[i][j][1] <= cr[1]:
                    channel_1 = cr
                if cr[0] <= img[i][j][2] <= cr[1]:
                    channel_2 = cr
                if channel_0 is not None and channel_1 is not None and channel_2 is not None:
                    break
            histogram[(channel_0, channel_1, channel_2)] += 1
            color_pixels[(channel_0, channel_1, channel_2)].append([i, j])

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
    return gamma


def calc_gamma(k, pixels):
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
