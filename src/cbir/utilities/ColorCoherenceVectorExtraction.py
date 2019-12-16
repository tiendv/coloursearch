import math
import cv2
import numpy as np
from scipy.ndimage.measurements import label
import collections
from ..models.ColorCoherenceVector import ColorCoherenceVector


def extract_color_coherence_vector(img_extraction_id, image_location, number_of_colors=512, tau=100):
    print('Extracting CCV for ' + image_location)
    number_of_ranges = number_of_colors ** (1 / 3)
    if (math.ceil(number_of_ranges) - number_of_ranges) < 0.001:
        number_of_ranges = math.ceil(number_of_ranges)
    else:
        number_of_ranges = int(number_of_ranges)

    colors = []

    for i in range(0, number_of_ranges + 1):
        for j in range(0, number_of_ranges + 1):
            for k in range(0, number_of_ranges + 1):
                colors.append([i, j, k])

    colors = np.array(colors)

    img = cv2.imread(image_location)
    image_height = len(img)
    image_width = len(img[0])

    blurred_image = np.array([[[0, 0, 0] for j in range(0, image_width)] for i in range(0, image_height)])

    # blur the image
    for k in range(0, 3):
        # 4 corner pixels
        blurred_image[0][0][k] = round((img[0][1][k] + img[1][0][k] + img[1][1][k]) / 3)
        blurred_image[0][image_width - 1][k] = round((img[0][image_width - 2][k]
                                                      + img[1][image_width - 1][k] + img[1][image_width - 2][k]) / 3)
        blurred_image[image_height - 1][0][k] = round((img[image_height - 1][1][k]
                                                       + img[image_height - 1][0][k] + img[image_height - 2][1][k]) / 3)
        blurred_image[image_height - 1][image_width - 1][k] = round((img[image_height - 1][image_width - 2][k]
                                                                     + img[image_height - 2][image_width - 1][k] +
                                                                     img[image_height - 2][image_width - 2][k]) / 3)

        # pixels in 4 bounds
        for j in range(1, image_width - 2):
            blurred_image[0][j][k] = round((img[0][j - 1][k] + img[0][j + 1][k]
                                            + img[1][j - 1][k] + img[1][j][k] + img[1][j + 1][k]) / 5)
            blurred_image[image_height - 1][j][k] = round((img[image_height - 1][j - 1][k]
                                                           + img[image_height - 1][j + 1][k] +
                                                           img[image_height - 2][j - 1][k]
                                                           + img[image_height - 2][j][k] + img[image_height - 2][j + 1][
                                                               k]) / 5)
        for i in range(1, image_height - 2):
            blurred_image[i][0][k] = round((img[i - 1][0][k] + img[i + 1][0][k]
                                            + img[i - 1][1][k] + img[i][1][k] + img[i + 1][1][k]) / 5)
            blurred_image[i][image_width - 1][k] = round((img[i - 1][image_width - 1][k]
                                                          + img[i + 1][image_width - 1][k] +
                                                          img[i - 1][image_width - 2][k]
                                                          + img[i][image_width - 2][k] + img[i + 1][image_width - 2][
                                                              k]) / 5)

        # remaining pixels
        for i in range(1, image_height - 2):
            for j in range(1, image_width - 2):
                blurred_image[i][j][k] = round((img[i - 1][j - 1][k] + img[i][j - 1][k] + img[i + 1][j - 1][k]
                                                + img[i - 1][j][k] + img[i + 1][j][k]
                                                + img[i - 1][j + 1][k] + img[i][j + 1][k] + img[i + 1][j + 1][k]) / 8)

    for k in range(0, 3):
        for i in range(0, image_height):
            for j in range(0, image_width):
                blurred_image[i][j][k] = round(blurred_image[i][j][k] / 255 * number_of_ranges)

    blurred_image.astype(np.int64)

    ccv = {
        tuple(color): {
            'alpha': 0,
            'beta': 0
        } for color in colors
    }

    for color in colors:
        labeled_image = [[1 if (blurred_image[i][j] == color).all() else 0 for j in range(0, image_width)] for i in
                         range(0, image_height)]
        structure = np.ones((3, 3), dtype=np.int)
        labeled, ncomponents = label(labeled_image, structure)
        labeled = labeled.reshape(-1)
        pixels = collections.Counter(labeled)
        color_tuple = tuple(color)
        for key, value in pixels.items():
            if key != 0:
                if value >= tau:
                    ccv[color_tuple]['alpha'] += value
                else:
                    ccv[color_tuple]['beta'] += value

    for key, value in ccv.items():
        instance = ColorCoherenceVector()
        instance.image_extraction_id = img_extraction_id
        instance.ccomponent1 = key[0]
        instance.ccomponent2 = key[1]
        instance.ccomponent3 = key[2]
        instance.alpha = value['alpha']
        instance.beta = value['beta']
        instance.save()
        print('Saved ' + str(key) + ': ' + str(value))

    return ccv


