import os
import cv2
import csv
import numpy as np
import collections
from ..constants import *
from django.conf import settings
from ..utilities.Utilities import image_resize


def annotate(directory_path):
    print('Annotating directory: {}.'.format(directory_path))
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
                  os.path.isfile(os.path.join(directory_path, f))]
    folder_name = os.path.basename(directory_path)

    csv_file_name = '{}.csv'.format(folder_name)
    csv_file_path = os.path.join(settings.BASE_DIR, csv_file_name)
    with open(csv_file_path, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            print('Annotating image file: {}.'.format(file_name))
            img = cv2.imread(file_path)
            height, width = img.shape[:2]
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
            Z = img.reshape((-1, 3))

            # convert to np.float32
            Z = np.float32(Z)

            # define criteria, number of clusters(K) and apply kmeans()
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            ret, label, center = cv2.kmeans(Z, K_IN_K_MEANS, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            center = cv2.cvtColor(np.asarray([center]), cv2.COLOR_BGR2HSV)
            center = center[0].tolist()
            label = label.flatten()
            colors = {}
            count = collections.Counter(list(label))
            count = count.most_common(4)
            count = sorted(count, key=lambda x: int(x[1]), reverse=True)
            color_indices = [item[0] for item in count]
            colors = []
            for i in color_indices:
                colors.append(center[i])
            colors = [convert_color_to_string(item) for item in colors]
            row = [file_name] + colors

            print('Value: {}.'.format(row))

            writer.writerows([row])

    print('Annotation file saved in {}.'.format(csv_file_path))

    return True


def convert_color_to_string(color):
    if color[2] < 35:
        return 'black'
    if color[1] < 35:
        return 'white'
    if color[0] <= 15 or color[0] > 165:
        return 'red'
    if 15 < color[0] <= 35:
        return 'yellow'
    if 35 < color[0] <= 85:
        return 'green'
    if 85 < color[0] <= 105:
        return 'cyan'
    if 105 < color[0] <= 135:
        return 'blue'
    if 135 < color[0] <= 165:
        return 'magenta'
