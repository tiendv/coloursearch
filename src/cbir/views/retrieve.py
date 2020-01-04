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
from django.http import HttpResponseRedirect, JsonResponse
from ..constants import *
from ..views.annotate import annotate, image_resize, get_dominant_color
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..models import Extraction, ImageExtraction, FuzzyColorHistogram
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space


def calc_similarity(fch, directory_path, fch_of_images, images, index):
    fch_of_image = [item['value'] for item in fch_of_images if item['image_extraction_id'] == images[index]['id']]
    # fch_of_image = np.float32(fch_of_image)
    similarity = 0.0
    if len(fch) == len(fch_of_image):
        for i in range(len(fch)):
            similarity += (fch[i] - fch_of_image[i]) ** 2
        # similarity = cv2.norm(fch - fch_of_image, cv2.NORM_L2)
    similarity = math.sqrt(similarity)
    return {
        'image_path': str(os.path.join(directory_path, images[index]['image_name'])),
        'thumbnail_path': str(images[index]['thumbnail_path']),
        'similarity': similarity
    }


def retrieve(request):
    start_time = time.time()
    if request.method == 'POST':
        colors = []
        if 'colorMap' in request.POST:
            colorMap = json.loads(request.POST.get('colorMap'))
            for row in colorMap:
                color_row = []
                for color in row:
                    color = list(map(int, color[4:-1].replace(' ', '').split(',')))
                    color_row.append(color)
                colors.append(color_row)
            image = np.uint8(colorMap)
            dominant_colors = get_dominant_color(image)
            print(dominant_colors)
        elif len(request.FILES) > 0:
            image = request.FILES['image']
            image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
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
            print('Resize to {}x{}'.format(image.shape[0], image.shape[1]))
            print("--- Resize: %s seconds ---" % (time.time() - start_time))

            dominant_colors = get_dominant_color(image)
            print(dominant_colors)
            colorMap = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            colors = colorMap.tolist()
        else:
            return
        print("--- Get dominant color and preprocessing: %s seconds ---" % (time.time() - start_time))

        method = request.POST.get('method')
        print(method)

        extraction_ids = json.loads(request.POST.get('extraction_id'))
        if len(extraction_ids) == 0:
            extraction_ids = Extraction.objects.values('id').order_by('id')
            extraction_ids = [item['id'] for item in extraction_ids]
        else:
            extraction_ids = [int(item) for item in extraction_ids]
        print(extraction_ids)

        if method == 'Fuzzy Color Histogram':
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
            print(csv_file)
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
            images_map = {}
            extractions = Extraction.objects\
                .filter(id__in=extraction_ids,
                        param1_value=number_of_coarse_colors,
                        param2_value=number_of_fine_colors,
                        param3_value=m)\
                .values('id', 'directory_path')

            result = []

            for extraction in extractions:
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
                print(csv_file)
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
                print('length of image list: {}'.format(len(list_of_image_name)))

                images = ImageExtraction.objects\
                    .filter(extraction_id=extraction['id'],
                            image_name__in=list_of_image_name)\
                    .values('id', 'image_name', 'thumbnail_path')
                image_ids = [item['id'] for item in images]
                images = list(images)
                print("--- Get images: %s seconds ---" % (time.time() - start_time))
                fch_of_images = FuzzyColorHistogram.objects\
                    .filter(image_extraction_id__in=image_ids)\
                    .values('image_extraction_id', 'id', 'value')\
                    .order_by('id')
                fch_of_images = list(fch_of_images)
                print("--- Get FCH: %s seconds ---" % (time.time() - start_time))

                import django
                django.setup()
                pool = multiprocessing.Pool(multiprocessing.cpu_count() - 2)
                result = pool.map(functools.partial(calc_similarity,
                                                    fch,
                                                    extraction['directory_path'],
                                                    fch_of_images,
                                                    images), range(0, len(images), 1))
                result = list(result)
                print(result)

                result = sorted(result, key=lambda k: k['similarity'])
                print("--- Retrieval: %s seconds ---" % (time.time() - start_time))
                return JsonResponse(result, safe=False)

                # for index, image in enumerate(images, start=1):
                #     images_map[image['id']] = calc_similarity(image, fch, extraction, fch_of_images)
                #     print('{}/{}. Degree of similarity ({}): {}'.format(index, len(list_of_image_name), image['image_name'], images_map[image['id']]['similarity']))

            # for key, value in images_map.items():
            #     result.append(value)

        elif method == 'Color Coherence Vector':
            extract_color_coherence_vector(-1, colorMap)
        elif method == 'Color Correlogram':
            extract_color_correlogram(-1, colorMap)
        elif method == 'Cumulative Color Histogram':
            extract_cumulative_color_histogram(-1, colorMap)
        return HttpResponseRedirect('/')


def evaluate_performance(database_name, query_folder_path, extraction_id):
    image_paths = []
    m_ap = {}
    m_ar = {}
    start_time = time.time()
    for dirpath, _, filenames in os.walk(query_folder_path):
        for f in filenames:
            image_paths.append(os.path.abspath(os.path.join(dirpath, f)))

    for index, image_path in enumerate(image_paths, start=1):
        colors = []
        print('{}/{}. Querying {}'.format(index, len(image_paths), image_path))
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        image = cv2.imread(image_path)
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
            images_map = {}
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
            result = list(result)

            result = sorted(result, key=lambda k: k['similarity'])
            print("Retrieval: %s seconds" % (time.time() - start_time))
            result = result[:6]
            query_precision = []
            query_recall = []
            number_of_relevant_images = 0
            if database_name == 'holidays':
                query_name_id = int(image_name)
            elif database_name == 'ukbench':
                query_name_id = int(image_name.replace('ukbench', ''))
                m_ap_key = query_name_id // 4 * 4
                if m_ap_key not in m_ap:
                    m_ap[m_ap_key] = []
                    m_ar[m_ap_key] = []
                for i, item in enumerate(result, start=1):
                    item_name = os.path.splitext(os.path.basename(item['image_path']))[0]
                    name_id = int(item_name.replace('ukbench', ''))
                    if (query_name_id // 4) == (name_id // 4):
                        number_of_relevant_images += 1
                        query_recall.append(number_of_relevant_images / 4)
                        query_precision.append(number_of_relevant_images / i)
                average_precision = sum(query_precision) / len(query_precision)
                average_recall = sum(query_recall) / len(query_recall)
                m_ap[m_ap_key].append(average_precision)
                m_ar[m_ap_key].append(average_recall)
    result = []
    for key, value in m_ap:
        result.append(sum(value) / len(value))
    result = sum(result) / len(result)
    print('----------------------')
    print('| MAP = {} |'.format(result))
    print('----------------------')
    return
