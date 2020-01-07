import os
import cv2
import csv
import json
import math
import time
import functools
import collections
import numpy as np
import multiprocessing
from django.conf import settings
from ..constants import *
from .retrieve import calc_similarity
from ..views.annotate import image_resize, get_dominant_color
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
from ..models import Extraction, ImageExtraction, FuzzyColorHistogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space


def evaluate(database_name, query_folder_path, extraction_id, k, type):
    image_paths = []
    m_ap = {}
    m_ar = {}
    for dirpath, _, filenames in os.walk(query_folder_path):
        for f in filenames:
            image_paths.append(os.path.abspath(os.path.join(dirpath, f)))

    for index, image_path in enumerate(image_paths, start=1):
        start_time = time.time()
        colors = []
        print('[{}/{}]. Querying {}'.format(index, len(image_paths), image_path))
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        image = cv2.imread(image_path)
        if type == 'image':
            height, width = image.shape[:2]
            if width > MAX_RETRIEVAL_IMAGE_WIDTH:
                image = image_resize(image, width=MAX_RETRIEVAL_IMAGE_WIDTH)
                height, width = image.shape[:2]
                if height > MAX_RETRIEVAL_IMAGE_HEIGHT:
                    image = image_resize(image, height=MAX_RETRIEVAL_IMAGE_HEIGHT)
            elif height > MAX_RETRIEVAL_IMAGE_HEIGHT:
                image = image_resize(image, height=MAX_RETRIEVAL_IMAGE_HEIGHT)
                height, width = image.shape[:2]
                if width > MAX_RETRIEVAL_IMAGE_WIDTH:
                    image = image_resize(image, width=MAX_RETRIEVAL_IMAGE_WIDTH)
        elif type == 'color_layout':
            image = image_resize(image, width=30)
            Z = image.reshape((-1, 3))

            # convert to np.float32
            Z = np.float32(Z)

            # define criteria, number of clusters(K) and apply kmeans()
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            ret, label, center = cv2.kmeans(Z, 16, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

            # Now convert back into uint8, and make original image
            center = np.uint8(center)
            res = center[label.flatten()]
            image_shape = image.shape
            image = res.reshape(image_shape)

            # For debugging
            res2 = image.reshape(-1, 3)
            res2 = res2.tolist()
            count = collections.Counter(tuple(item) for item in res2)
            print(count)

        dominant_colors = get_dominant_color(image)
        print(dominant_colors)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        colors = image.tolist()
        print("Get dominant color and preprocessing: %s seconds" % (time.time() - start_time))

        method = Extraction.objects\
            .filter(id=extraction_id)\
            .values('method_id')
        method = method[0]['method_id']
        print(method)

        if method == 'fuzzy_color_histogram':
            number_of_coarse_colors = NUMBER_OF_COARSE_COLORS
            number_of_fine_colors = NUMBER_OF_FINE_COLORS
            m = M
            matrix_path = os.path.join(settings.BASE_DIR, 'matrix')
            csv_file = ''
            for r, d, f in os.walk(matrix_path):
                for file in f:
                    if '.csv' in file:
                        file_name = os.path.splitext(file)[0]
                        color_name = '_'.join(map(str, [NUMBER_OF_COARSE_COLORS, NUMBER_OF_FINE_COLORS]))
                        if file_name == color_name:
                            csv_file = os.path.join(r, file)
            if csv_file == '':
                coarse_color_ranges, coarse_channel_ranges, matrix, v = quantize_color_space()
            else:
                v = FuzzyColorHistogramColor.objects\
                    .filter(number_of_coarse_colors=NUMBER_OF_COARSE_COLORS,
                            number_of_fine_colors=NUMBER_OF_FINE_COLORS)\
                    .values('ccomponent1', 'ccomponent2', 'ccomponent3')
                v = [[item['ccomponent1'], item['ccomponent2'], item['ccomponent3']] for item in v]
                with open(csv_file) as csv_file:
                    csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_ALL)
                    matrix = list(csv_reader)
                coarse_color_ranges, coarse_colors, coarse_channel_ranges = calc_color_range(NUMBER_OF_COARSE_COLORS)
            fch = extract_fuzzy_color_histogram(-1,
                                                colors,
                                                coarse_color_ranges,
                                                coarse_channel_ranges,
                                                matrix, v)
            # fch = np.float32(fch)
            extraction = Extraction.objects\
                .filter(id=extraction_id,
                        param1_value=number_of_coarse_colors,
                        param2_value=number_of_fine_colors,
                        param3_value=m)\
                .values('id', 'directory_path')

            extraction = extraction[0]
            result = []
            directory_path = extraction['directory_path']
            folder_name = os.path.basename(directory_path)

            annotation_path = os.path.join(settings.BASE_DIR, 'annotation')
            csv_file = ''
            for r, d, f in os.walk(annotation_path):
                for file in f:
                    if '.csv' in file:
                        file_name = os.path.splitext(file)[0]
                        if file_name == folder_name:
                            csv_file = os.path.join(r, file)
                            break
            with open(csv_file) as csv_file:
                csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_ALL)
                color_matrix = list(csv_reader)
            list_of_image_name = []
            for row in color_matrix:
                if row[1] in dominant_colors:
                    list_of_image_name.append(row[0])
                    continue
                if row[2] in dominant_colors:
                    list_of_image_name.append(row[0])
                    continue
                if row[3] in dominant_colors:
                    list_of_image_name.append(row[0])
                    continue
                if row[4] in dominant_colors:
                    list_of_image_name.append(row[0])
                    continue
            print('Length of image list: {}'.format(len(list_of_image_name)))

            images = ImageExtraction.objects\
                .filter(extraction_id=extraction['id'],
                        image_name__in=list_of_image_name)\
                .values('id', 'image_name', 'thumbnail_path')
            image_ids = [item['id'] for item in images]
            images = list(images)
            print("Get images list: %s seconds" % (time.time() - start_time))
            fch_of_images = FuzzyColorHistogram.objects\
                .filter(image_extraction_id__in=image_ids)\
                .values('image_extraction_id', 'id', 'value')\
                .order_by('id')
            fch_of_images = list(fch_of_images)
            print("Get FCH: %s seconds" % (time.time() - start_time))

            import django
            django.setup()
            pool = multiprocessing.Pool(multiprocessing.cpu_count() - 2)
            result = pool.map(functools.partial(calc_similarity,
                                                fch,
                                                extraction['directory_path'],
                                                fch_of_images,
                                                images), range(0, len(images), 1))
            pool.close()
            pool.join()
            result = list(result)

            result = sorted(result, key=lambda k: k['similarity'])
            print("Retrieval: %s seconds" % (time.time() - start_time))
            result = result[:k]
            query_precision = []
            query_recall = []
            number_of_relevant_images = 0
            m_ap_key = None
            query_name_id = None

            if database_name == 'holidays':
                query_name_id = int(image_name)
                m_ap_key = query_name_id // 100 * 100
            elif database_name == 'ukbench':
                query_name_id = int(image_name.replace('ukbench', ''))
                m_ap_key = query_name_id // 4 * 4

            if m_ap_key not in m_ap:
                m_ap[m_ap_key] = []
                m_ar[m_ap_key] = []
            for i, item in enumerate(result, start=1):
                item_name = os.path.splitext(os.path.basename(item['image_path']))[0]
                if database_name == 'holidays':
                    name_id = int(item_name)
                    if (query_name_id // 4) == (name_id // 4):
                        number_of_relevant_images += 1
                        query_recall.append(number_of_relevant_images / 4)
                        query_precision.append(number_of_relevant_images / i)
                elif database_name == 'ukbench':
                    name_id = int(item_name.replace('ukbench', ''))
                    if (query_name_id // 100) == (name_id // 100):
                        number_of_relevant_images += 1
                        query_recall.append(number_of_relevant_images / 4)
                        query_precision.append(number_of_relevant_images / i)
            print('|- Query precision -|')
            print(query_precision)
            print('|- Query recall -|')
            print(query_recall)
            average_precision = 0
            average_recall = 0
            if len(query_precision) != 0:
                average_precision = sum(query_precision) / len(query_precision)
            if len(query_recall) != 0:
                average_recall = sum(query_recall) / len(query_recall)
            m_ap[m_ap_key].append(average_precision)
            m_ar[m_ap_key].append(average_recall)
            print('--- m_ap ---')
            print(m_ap)
            print('--- m_ar ---')
            print(m_ar)
    result = []
    for key, value in m_ap.items():
        if len(value) != 0:
            result.append(sum(value) / len(value))
        else:
            result.append(0)
    if len(result) != 0:
        result = sum(result) / len(result)
    else:
        result = 0
    print('-----------------------------')
    print('| MAP = {} |'.format(result))
    print('-----------------------------')
    return
