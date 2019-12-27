import math
import cv2
import time
import numpy as np
import collections
from scipy.ndimage.measurements import label
from ..models.ColorCoherenceVector import ColorCoherenceVector


def quantize_color(img, n=64):
    div = 256 // n
    rgb = cv2.split(img)
    q = []
    for ch in rgb:
        vf = np.vectorize(lambda x, div: int(x // div) * div)
        quantized = vf(ch, div)
        q.append(quantized.astype(np.uint8))
    d_img = cv2.merge(q)
    return d_img


def extract_color_coherence_vector(img_extraction_id, image_location, number_of_colors=128, tau=100):
    number_of_colors = int(number_of_colors)
    tau = int(tau)

    print('Extracting CCV for ' + image_location)
    print('number_of_colors = ' + str(number_of_colors))
    print('tau = ' + str(tau))

    start_time = time.time()
    img = cv2.imread(image_location)
    row, col, channels = img.shape

    blurred_image = cv2.GaussianBlur(img, (3, 3), 0)
    blurred_image = blurred_image.astype(np.int64)
    img = quantize_color(img, number_of_colors)
    lab = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2Lab))

    if tau == 0:
        tau = row * col * 0.1
    alpha = np.zeros(number_of_colors)
    beta = np.zeros(number_of_colors)

    for i, ch in enumerate(lab):
        ret, th = cv2.threshold(ch, 127, 255, 0)
        ret, labeled, stat, centroids = cv2.connectedComponentsWithStats(th, None, cv2.CC_STAT_AREA, None,
                                                                         connectivity=8)
        # !see https://github.com/atinfinity/lab/wiki/OpenCV%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E3%83%A9%E3%83%99%E3%83%AA%E3%83%B3%E3%82%B0#samplecode
        # !see http://docs.opencv.org/3.0.0/d3/dc0/group__imgproc__shape.html#gac7099124c0390051c6970a987e7dc5c5
        # generate ccv
        areas = [[v[4], label_idx] for label_idx, v in enumerate(stat)]
        coord = [[v[0], v[1]] for label_idx, v in enumerate(stat)]

        # Counting
        for a, c in zip(areas, coord):
            area_size = a[0]
            x, y = c[0], c[1]
            if (x < ch.shape[1]) and (y < ch.shape[0]):
                bin_idx = int(ch[y, x] // (256 // number_of_colors))
                if area_size >= tau:
                    alpha[bin_idx] = alpha[bin_idx] + area_size
                else:
                    beta[bin_idx] = beta[bin_idx] + area_size

    ccv = {
        tuple([0, 0, i]): {
            'alpha': alpha[i],
            'beta': beta[i]
        } for i in range(0, number_of_colors)
    }

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

    print("--- Extraction time: %s seconds ---" % (time.time() - start_time))
    return ccv


# def extract_color_coherence_vector(img_extraction_id, image_location, number_of_colors=512, tau=100):
#     print('Extracting CCV for ' + image_location)
#     print('number_of_colors = ' + str(number_of_colors))
#     print('tau = ' + str(tau))
#     number_of_ranges = number_of_colors ** (1 / 3)
#     if (math.ceil(number_of_ranges) - number_of_ranges) < 0.001:
#         number_of_ranges = math.ceil(number_of_ranges)
#     else:
#         number_of_ranges = int(number_of_ranges)
#
#     colors = []
#
#     for i in range(0, number_of_ranges + 1):
#         for j in range(0, number_of_ranges + 1):
#             for k in range(0, number_of_ranges + 1):
#                 colors.append([i, j, k])
#
#     colors = np.array(colors)
#
#     img = cv2.imread(image_location)
#     image_height = len(img)
#     image_width = len(img[0])
#
#     blurred_image = np.array([[[0, 0, 0] for j in range(0, image_width)] for i in range(0, image_height)])
#
#     # blur the image
#     for k in range(0, 3):
#         # 4 corner pixels
#         blurred_image[0][0][k] = round((img[0][1][k] + img[1][0][k] + img[1][1][k]) / 3)
#         blurred_image[0][image_width - 1][k] = round((int(img[0][image_width - 2][k])
#                                                       + int(img[1][image_width - 1][k]) + int(img[1][image_width - 2][k])) / 3)
#         blurred_image[image_height - 1][0][k] = round((int(img[image_height - 1][1][k])
#                                                        + int(img[image_height - 1][0][k]) + int(img[image_height - 2][1][k])) / 3)
#         blurred_image[image_height - 1][image_width - 1][k] = round((int(img[image_height - 1][image_width - 2][k])
#                                                                      + int(img[image_height - 2][image_width - 1][k]) +
#                                                                      int(img[image_height - 2][image_width - 2][k])) / 3)
#
#         # pixels in 4 bounds
#         for j in range(1, image_width - 2):
#             blurred_image[0][j][k] = round((img[0][j - 1][k] + img[0][j + 1][k]
#                                             + img[1][j - 1][k] + img[1][j][k] + img[1][j + 1][k]) / 5)
#             blurred_image[image_height - 1][j][k] = round((img[image_height - 1][j - 1][k]
#                                                            + img[image_height - 1][j + 1][k] +
#                                                            img[image_height - 2][j - 1][k]
#                                                            + img[image_height - 2][j][k] + img[image_height - 2][j + 1][
#                                                                k]) / 5)
#         for i in range(1, image_height - 2):
#             blurred_image[i][0][k] = round((img[i - 1][0][k] + img[i + 1][0][k]
#                                             + img[i - 1][1][k] + img[i][1][k] + img[i + 1][1][k]) / 5)
#             blurred_image[i][image_width - 1][k] = round((img[i - 1][image_width - 1][k]
#                                                           + img[i + 1][image_width - 1][k] +
#                                                           img[i - 1][image_width - 2][k]
#                                                           + img[i][image_width - 2][k] + img[i + 1][image_width - 2][
#                                                               k]) / 5)
#
#         # remaining pixels
#         for i in range(1, image_height - 2):
#             for j in range(1, image_width - 2):
#                 blurred_image[i][j][k] = round((img[i - 1][j - 1][k] + img[i][j - 1][k] + img[i + 1][j - 1][k]
#                                                 + img[i - 1][j][k] + img[i + 1][j][k]
#                                                 + img[i - 1][j + 1][k] + img[i][j + 1][k] + img[i + 1][j + 1][k]) / 8)
#
#     for k in range(0, 3):
#         for i in range(0, image_height):
#             for j in range(0, image_width):
#                 blurred_image[i][j][k] = round(blurred_image[i][j][k] / 255 * number_of_ranges)
#
#     blurred_image.astype(np.int64)
#
#     ccv = {
#         tuple(color): {
#             'alpha': 0,
#             'beta': 0
#         } for color in colors
#     }
#
#     for color in colors:
#         labeled_image = [[1 if (blurred_image[i][j] == color).all() else 0 for j in range(0, image_width)] for i in
#                          range(0, image_height)]
#         structure = np.ones((3, 3), dtype=np.int)
#         labeled, ncomponents = label(labeled_image, structure)
#         labeled = labeled.reshape(-1)
#         pixels = collections.Counter(labeled)
#         color_tuple = tuple(color)
#         for key, value in pixels.items():
#             if key != 0:
#                 if value >= tau:
#                     ccv[color_tuple]['alpha'] += value
#                 else:
#                     ccv[color_tuple]['beta'] += value
#
#     for key, value in ccv.items():
#         instance = ColorCoherenceVector()
#         instance.image_extraction_id = img_extraction_id
#         instance.ccomponent1 = key[0]
#         instance.ccomponent2 = key[1]
#         instance.ccomponent3 = key[2]
#         instance.alpha = value['alpha']
#         instance.beta = value['beta']
#         instance.save()
#         print('Saved ' + str(key) + ': ' + str(value))
#
#     return ccv


