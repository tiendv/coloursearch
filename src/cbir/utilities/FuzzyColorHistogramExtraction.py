import os
import csv
import math
import numpy as np
from django.conf import settings
from .ColorHistogramExtraction import *
from ..models import FuzzyColorHistogram, FuzzyColorHistogramColor


def quantize_color_space(number_of_coarse_colors=4096, number_of_fine_colors=64, m=1.9):
    print('Quantizing color space... Waiting...')
    coarse_color_ranges, coarse_colors, coarse_channel_ranges = calc_color_range(number_of_coarse_colors)
    fine_color_ranges, fine_colors, fine_channel_ranges = calc_color_range(number_of_fine_colors)

    number_of_coarse_colors = len(coarse_colors)
    number_of_fine_colors = len(fine_colors)

    iterator_count = 0
    epsilon = 10
    u = [[0.0 for k in range(number_of_coarse_colors)] for i in range(number_of_fine_colors)]

    for i in range(0, number_of_fine_colors):
        for k in range(0, number_of_coarse_colors):
            d = 0
            for j in range(0, number_of_fine_colors):
                f1 = math.sqrt((coarse_colors[k][0] - fine_colors[i][0])**2 +
                               (coarse_colors[k][1] - fine_colors[i][1])**2 +
                               (coarse_colors[k][2] - fine_colors[i][2])**2)

                f2 = math.sqrt((coarse_colors[k][0] - fine_colors[j][0])**2 +
                               (coarse_colors[k][1] - fine_colors[j][1])**2 +
                               (coarse_colors[k][2] - fine_colors[j][2])**2)
                d += (math.pow((f1 / f2), (1.0 / (m - 1))))
            if d != 0:
                u[i][k] = 1.0 / d
            else:
                u[i][k] = 0.0
        print('Calculating fine color i = ' + str(i))

    v = [[color[0], color[1], color[2]] for color in fine_colors]
    x = [[color[0], color[1], color[2]] for color in coarse_colors]
    u_e = [[u[i][k] for k in range(number_of_coarse_colors)] for i in range(number_of_fine_colors)]

    while True:
        # Update v
        for i in range(0, number_of_fine_colors):
            n0 = n1 = n2 = d = d = d = 0
            for k in range(0, number_of_coarse_colors):
                n0 += math.pow(u[i][k], m) * x[k][0]
                n1 += math.pow(u[i][k], m) * x[k][1]
                n2 += math.pow(u[i][k], m) * x[k][2]
                d += u[i][k]**m

            if d != 0:
                v[i][0] = 1.0 * n0 / d
                v[i][1] = 1.0 * n1 / d
                v[i][2] = 1.0 * n2 / d

        # Update u
        for i in range(0, number_of_fine_colors):
            for k in range(0, number_of_coarse_colors):
                d = 0
                for j in range(0, number_of_fine_colors):
                    f1 = math.sqrt((coarse_colors[k][0] - fine_colors[i][0]) ** 2 +
                                   (coarse_colors[k][1] - fine_colors[i][1]) ** 2 +
                                   (coarse_colors[k][2] - fine_colors[i][2]) ** 2)

                    f2 = math.sqrt((coarse_colors[k][0] - fine_colors[j][0]) ** 2 +
                                   (coarse_colors[k][1] - fine_colors[j][1]) ** 2 +
                                   (coarse_colors[k][2] - fine_colors[j][2]) ** 2)
                    d += (math.pow((f1 / f2), (1.0 / (m - 1))))
                if d != 0:
                    u[i][k] = 1.0 / d
                else:
                    u[i][k] = 0.0
        print('Matrix calculation done.')

        # Calculate error tolerance
        error_tolerance = 0.0
        for i in range(0, number_of_fine_colors):
            for k in range(0, number_of_coarse_colors):
                error_tolerance += (u[i][k] - u_e[i][k])**2
        error_tolerance = math.sqrt(error_tolerance)

        iterator_count += 1

        if error_tolerance <= epsilon:
            break
        else:
            u_e = [[u[i][k] for k in range(number_of_coarse_colors)] for i in range(number_of_fine_colors)]
    matrix = np.asarray(u)

    existed_color = FuzzyColorHistogramColor.objects\
        .filter(number_of_coarse_colors=number_of_coarse_colors, number_of_fine_colors=number_of_fine_colors)
    if len(existed_color) == 0:
        for i in range(0, len(v)):
            instance = FuzzyColorHistogramColor()
            instance.number_of_fine_colors = number_of_fine_colors
            instance.number_of_coarse_colors = number_of_coarse_colors
            instance.ccomponent1 = v[i][0]
            instance.ccomponent2 = v[i][1]
            instance.ccomponent3 = v[i][2]
            instance.save()

    file_name = '{}_{}.csv'.format(number_of_coarse_colors, number_of_fine_colors)
    file_path = os.path.join(settings.BASE_DIR, 'matrix', file_name)
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(matrix)
        print('Matrix saved in {}.'.format(file_path))

    return coarse_color_ranges, coarse_channel_ranges, matrix, v


def extract_fuzzy_color_histogram(img_extraction_id, image_location, coarse_color_ranges, coarse_channel_ranges, matrix, v):
    if type(image_location) == str:
        print('Extracting FCH for ' + image_location)
    cielab_color_histogram = extract_cielab_color_histogram(image_location, coarse_color_ranges, coarse_channel_ranges)
    cch = []
    for key, value in cielab_color_histogram.items():
        cch.append(value)
    cch = np.asarray(cch, dtype=np.float32)
    membership_matrix = np.asarray(matrix, dtype=np.float32)

    fch = None
    if len(membership_matrix.shape) == 2:
        if membership_matrix.shape[1] == len(cch):
            fch = np.dot(cch, membership_matrix.T)
            if img_extraction_id != -1:
                for i in range(0, len(v)):
                    c1 = v[i][0]
                    c2 = v[i][1]
                    c3 = v[i][2]
                    color_id = FuzzyColorHistogramColor.objects \
                        .filter(number_of_coarse_colors=len(cch), number_of_fine_colors=len(v),
                                ccomponent1=c1, ccomponent2=c2, ccomponent3=c3).values('id').distinct()
                    if len(color_id) > 0:
                        instance = FuzzyColorHistogram(image_extraction_id=img_extraction_id)
                        color_id = list(color_id)[0]['id']
                        instance.color_id = color_id
                        instance.value = fch[i]
                        instance.save()
                return True
            else:
                return fch
    return False
