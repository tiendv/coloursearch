import os
import numpy as np
import cv2
from collections import Counter
from .. import constants
from django.shortcuts import render
from ..models import ColorHistogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram


def extract_features(request, *args, **kwargs):
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(f'Key: {key}')
            print(f'Value: {value}')

        folder_path = request.POST.get('folder_path')

        # r=root, d=directories, f = files
        images = []
        for r, d, f in os.walk(folder_path):
            for file in f:
                if ('.jpg' in file) or ('.png' in file):
                    images.append(os.path.join(r, file))
        i = 1
        for img in images:
            extract_fuzzy_color_histogram(img, 4096, 64, 1.9)
        #     img = cv2.imread(img)
        #     Z = img.reshape((-1, 3))
        #     Z = np.float32(Z)
        #
        #     # The iteration termination criteria
        #     # cv2.TERM_CRITERIA_EPS - stop the algorithm iteration if specified accuracy, epsilon, is reached.
        #     # cv2.TERM_CRITERIA_MAX_ITER - stop the algorithm after the specified number of iterations, max_iter.
        #     # cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER - stop the iteration when any of the above
        #     # condition is met.
        #     # max_iter - An integer specifying maximum number of iterations.
        #     # epsilon - Required accuracy
        #     # For each run, the algorithm will stop if:
        #     # The number of iteration reaches max_iter,
        #     # or every cluster center moved less than epsilon in the last iteration.
        #     criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        #     compactness, labels, centers = cv2.kmeans(Z, constants.K, None, criteria,
        #                                               10, cv2.KMEANS_RANDOM_CENTERS)
        #     centers = np.uint8(centers)
        #     res = centers[labels.flatten()]
        #     counts = dict(Counter(map(tuple, res)))
        #     object_dict = {'image_id': i}
        #     for field_name in constants.FIELD_NAMES:
        #         object_dict[field_name] = 0
        #     for key, value in counts.items():
        #         color = np.uint8([[list(key)]])
        #         color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)[0][0]
        #         color[0] = round(color[0] * 2 / 45.0) * 45
        #         color[1] = round(color[1] / 255.0 * 2) * 50
        #         color[2] = round(color[2] / 255.0 * 2) * 50
        #         field_name = 'c_' + str(color[0]) + '_' + str(color[1]) + '_' + str(color[2])
        #         if field_name in constants.FIELD_NAMES:
        #             object_dict[field_name] = object_dict[field_name] + value
        #     ColorHistogram.objects.create(**object_dict)
        #     i = i + 1

    return render(request, 'html/extract-features.html', {})
