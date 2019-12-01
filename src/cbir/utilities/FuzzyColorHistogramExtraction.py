import os
import numpy as np
import cv2
import math
from collections import Counter
from .. import constants
from django.shortcuts import render
from .ColorHistogramExtraction import calc_color_range, extract_rgb_color_histogram


def extract_fuzzy_color_histogram(image, number_of_coarse_color, number_of_fine_color, m):
    coarse_color_range, coarse_color, coarse_channel_range = calc_color_range(number_of_coarse_color)
    fine_color_range, fine_color,fine_channel_range = calc_color_range(number_of_fine_color)

    number_of_coarse_color = len(coarse_color)
    number_of_fine_color = len(fine_color)

    rgb_color_histogram = extract_rgb_color_histogram(image, coarse_color_range, coarse_channel_range)

    iterator_count = 0
    epsilon = 10
    u = [[0.0 for k in range(number_of_coarse_color)] for i in range(number_of_fine_color)]

    coarse_channel = []
    fine_channel = []

    for i in range(0, 3):
        coarse_channel.append(convert_to_channel(coarse_color, i))
        fine_channel.append(convert_to_channel(fine_color, i))

    for i in range(0, number_of_fine_color):
        for k in range(0, number_of_coarse_color):
            d = 0
            for j in range(0, number_of_fine_color):
                f1 = math.sqrt((coarse_color[k][0] - fine_color[i][0])**2 +
                               (coarse_color[k][1] - fine_color[i][1])**2 +
                               (coarse_color[k][2] - fine_color[i][2])**2)

                f2 = math.sqrt((coarse_color[k][0] - fine_color[j][0])**2 +
                               (coarse_color[k][1] - fine_color[j][1])**2 +
                               (coarse_color[k][2] - fine_color[j][2])**2)
                d += (math.pow((f1 / f2), (1.0 / (m - 1))))
            if d != 0:
                u[i][k] = 1.0 / d
            else:
                u[i][k] = 0.0
        print('i = ' + str(i))

    v = [(color[0], color[1], color[2]) for color in fine_color]
    x = [(color[0], color[1], color[2]) for color in coarse_color]
    u_e = [[u[i][k] for k in range(number_of_coarse_color)] for i in range(number_of_fine_color)]

    while True:
        # Update v
        for i in range(0, number_of_fine_color):
            n1 = n2 = n3 = d = d = d = 0
            for k in range(0, number_of_coarse_color):
                n1 += u[i][k]**m * x[k][1]
                n2 += u[i][k]**m * x[k][2]
                n3 += u[i][k]**m * x[k][3]
                d += u[i][k]**m

            if d != 0:
                v[i][0] = 1.0 * n1 / d
                v[i][1] = 1.0 * n1 / d
                v[i][2] = 1.0 * n1 / d

        # Update u
        for i in range(0, number_of_fine_color):
            for k in range(0, number_of_coarse_color):
                d = 0
                for j in range(0, number_of_fine_color):
                    f1 = math.sqrt((coarse_color[k][0] - fine_color[i][0]) ** 2 +
                                   (coarse_color[k][1] - fine_color[i][1]) ** 2 +
                                   (coarse_color[k][2] - fine_color[i][2]) ** 2)

                    f2 = math.sqrt((coarse_color[k][0] - fine_color[j][0]) ** 2 +
                                   (coarse_color[k][1] - fine_color[j][1]) ** 2 +
                                   (coarse_color[k][2] - fine_color[j][2]) ** 2)
                    d += (math.pow((f1 / f2), (1.0 / (m - 1))))
                if d != 0:
                    u[i][k] = 1.0 / d
                else:
                    u[i][k] = 0.0

        # Calculate error tolerance
        error_tolerance = 0.0
        for i in range(0, number_of_fine_color):
            for k in range(0, number_of_coarse_color):
                error_tolerance += (u[i][k] - u_e[i][k])**2
        error_tolerance = math.sqrt(error_tolerance)

        iterator_count += 1
        print(iterator_count)

        if error_tolerance <= epsilon:
            break
        else:
            u_e = [[u[i][k] for k in range(number_of_coarse_color)] for i in range(number_of_fine_color)]

    return v, u


def convert_to_channel(colors, channel):
    result = []
    for color in colors:
        result.append(color[channel])
    return result