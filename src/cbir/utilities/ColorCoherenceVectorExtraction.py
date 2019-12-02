import math
import cv2
from .ColorHistogramExtraction import calc_color_range, extract_rgb_color_histogram
import numpy as np
from scipy.ndimage.measurements import label


def extract_color_coherence_vector(image, number_of_color=512, tau=300):
    number_of_range = number_of_color ** (1 / 3)
    if (math.ceil(number_of_range) - number_of_range) < 0.001:
        number_of_range = math.ceil(number_of_range)
    else:
        number_of_range = int(number_of_range)

    color_range, color, channel_range = calc_color_range(number_of_color)
    img = cv2.imread(image)
    image_height = len(img)
    image_width = len(img[0])

    blurred_image = [[[0, 0, 0] for j in range(0, image_width)] for i in range(0, image_height)]

    # blur the image
    for k in range(0, 3):
        # 4 corner pixels
        blurred_image[0][0][k] = round((img[0][1][k] + img[1][0][k] + img[1][1][k]) / 3)
        blurred_image[0][image_width - 1][k] = round((img[0][image_width - 2][k]
                                                 + img[1][image_width - 1][k] + img[1][image_width - 2][k]) / 3)
        blurred_image[image_height - 1][0][k] = round((img[image_height - 1][1][k]
                                                  + img[image_height - 1][0][k] + img[image_height - 2][1][k]) / 3)
        blurred_image[image_height - 1][image_width - 1][k] = round((img[image_height - 1][image_width - 2][k]
                 + img[image_height - 2][image_width - 1][k] + img[image_height - 2][image_width - 2][k]) / 3)

        # pixels in 4 bounds
        for j in range(1, image_width - 2):
            blurred_image[0][j][k] = round((img[0][j - 1][k] + img[0][j + 1][k]
                                       + img[1][j - 1][k] + img[1][j][k] + img[1][j + 1][k]) / 5)
            blurred_image[image_height - 1][j][k] = round((img[image_height - 1][j - 1][k]
                                                 + img[image_height - 1][j + 1][k] + img[image_height - 2][j - 1][k]
                                                 + img[image_height - 2][j][k] + img[image_height - 2][j + 1][k]) / 5)
        for i in range(1, image_height - 2):
            blurred_image[i][0][k] = round((img[i - 1][0][k] + img[i + 1][0][k]
                                       + img[i - 1][1][k] + img[i][1][k] + img[i + 1][1][k]) / 5)
            blurred_image[i][image_width - 1][k] = round((img[i - 1][image_width - 1][k]
                                                + img[i + 1][image_width - 1][k] + img[i - 1][image_width - 2][k]
                                                + img[i][image_width - 2][k] + img[i + 1][image_width - 2][k]) / 5)

        # remaining pixels
        for i in range(1, image_height - 2):
            for j in range(1, image_width - 2):
                blurred_image[i][j][k] = round((img[i - 1][j - 1][k] + img[i][j - 1][k] + img[i + 1][j - 1][k]
                                              + img[i - 1][j][k] + img[i + 1][j][k]
                                              + img[i - 1][j + 1][k] + img[i][j + 1][k] + img[i + 1][j + 1][k]) / 8)

    for k in range(0, 3):
        for i in range(0, image_height - 1):
            for j in range(0, image_width - 1):
                blurred_image[i][j][k] = round(blurred_image[i][j][k] / 255 * number_of_range)

    for k in range(0, number_of_range):
        blurred_image_array = np.array(blurred_image)
        structure = np.ones((3, 3), dtype=np.int)
        labeled, ncomponents = label(blurred_image_array, structure)
        


