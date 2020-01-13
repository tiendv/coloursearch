import os
import cv2
import csv
import json
import math
import time
import faiss
import functools
import numpy as np
import multiprocessing
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from ..constants import *
from ..views.annotate import image_resize, get_dominant_color
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..models import Extraction, ImageExtraction, FuzzyColorHistogram, ColorCoherenceVector, ColorCorrelogram, \
    CumulativeColorHistogram
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space


def calc_fch_similarity(fch, directory_path, fch_of_images, images, index):
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


def calc_ccv_similarity(ccv, directory_path, ccv_of_images, images, index):
    alpha_of_image = [item['alpha'] for item in ccv_of_images if item['image_extraction_id'] == images[index]['id']]
    beta_of_image = [item['beta'] for item in ccv_of_images if item['image_extraction_id'] == images[index]['id']]
    similarity = 0.0
    if len(ccv) == len(alpha_of_image) and len(ccv) == len(beta_of_image):
        for i in range(len(ccv)):
            similarity += abs(ccv[(0, 0, i)]['alpha'] - alpha_of_image[i]) + abs(ccv[(0, 0, i)]['beta'] - beta_of_image[i])
        # similarity = cv2.norm(ccv - ccv_of_image, cv2.NORM_L2)
    return {
        'image_path': str(os.path.join(directory_path, images[index]['image_name'])),
        'thumbnail_path': str(images[index]['thumbnail_path']),
        'similarity': similarity / 1000000
    }


def calc_cc_similarity(cc, directory_path, cc_of_images, images, index):
    cc_of_image = [item['value'] for item in cc_of_images if item['image_extraction_id'] == images[index]['id']]
    similarity = 0.0
    if len(cc) == len(cc_of_image):
        for index, (key, value) in enumerate(cc.items()):
            similarity += abs(cc[value]['value'] - cc_of_image[index])
        # similarity = cv2.norm(ccv - ccv_of_image, cv2.NORM_L2)
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
            image = np.uint8(colors)
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

        result = []

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
            if csv_file == '':
                coarse_color_ranges, coarse_channel_ranges, matrix, v = quantize_color_space()
            else:
                v = FuzzyColorHistogramColor.objects \
                    .filter(number_of_coarse_colors=NUMBER_OF_COARSE_COLORS,
                            number_of_fine_colors=NUMBER_OF_FINE_COLORS) \
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
            extractions = Extraction.objects \
                .filter(id__in=extraction_ids,
                        param1_value=number_of_coarse_colors,
                        param2_value=number_of_fine_colors,
                        param3_value=m) \
                .values('id', 'directory_path')

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

                image_extractions = ImageExtraction.objects \
                    .filter(extraction_id=extraction['id'],
                            image_name__in=list_of_image_name) \
                    .values('id', 'image_name', 'thumbnail_path')
                image_ids = [item['id'] for item in image_extractions]
                image_extractions = list(image_extractions)
                print("--- Get images: %s seconds ---" % (time.time() - start_time))
                fch_of_images = FuzzyColorHistogram.objects \
                    .filter(image_extraction_id__in=image_ids) \
                    .values('image_extraction_id', 'id', 'value') \
                    .order_by('id')
                fch_of_images = list(fch_of_images)
                print("--- Get FCH: %s seconds ---" % (time.time() - start_time))

                import django
                django.setup()

                # faiss
                vector_dict = {}
                vector = []
                for item in fch_of_images:
                    vector_index = item['image_extraction_id']
                    if vector_index not in vector_dict:
                        vector_dict[vector_index] = []
                    vector_dict[vector_index].append(item['value'])
                for key, value in vector_dict.items():
                    vector.append(value)
                vector = np.asarray(vector).astype('float32')
                query = np.asarray([fch]).astype('float32')

                index = faiss.IndexFlatL2(NUMBER_OF_FINE_COLORS)
                index.add(vector)
                distance_array, index_array = index.search(query, 200)
                for i, item in enumerate(index_array[0]):
                    result.append({
                        'image_path': str(os.path.join(directory_path, image_extractions[item]['image_name'])),
                        'thumbnail_path': str(image_extractions[item]['thumbnail_path']),
                        'similarity': str(distance_array[0][i])
                    })

                # For production
                # pool = multiprocessing.Pool(multiprocessing.cpu_count() - 2)
                # result = pool.map(functools.partial(calc_fch_similarity,
                #                                     fch,
                #                                     extraction['directory_path'],
                #                                     fch_of_images,
                #                                     image_extractions), range(0, len(image_extractions), 1))
                # pool.close()
                # pool.join()

                # For local testing
                # result = []
                # for index in range(0, len(images)):
                #     result.append(calc_fch_similarity(fch, extraction['directory_path'], fch_of_images, images, index))

                # result = list(result)
                print(result)

                result = sorted(result, key=lambda k: k['similarity'])
                print("--- Retrieval: %s seconds ---" % (time.time() - start_time))

                # for index, image in enumerate(image_extractions, start=1):
                #     images_map[image['id']] = calc_fch_similarity(image, fch, extraction, fch_of_images)
                #     print('{}/{}. Degree of similarity ({}): {}'.format(index,
                #                                                         len(list_of_image_name),
                #                                                         image['image_name'],
                #                                                         images_map[image['id']]['similarity']))

            # for key, value in images_map.items():
            #     result.append(value)

        elif method == 'Color Coherence Vector':
            ccv_temp = extract_color_coherence_vector(-1, image)
            ccv = []
            for key, value in ccv_temp.items():
                ccv.append(value['alpha'])
            extraction_ids = [3]
            extractions = Extraction.objects \
                .filter(id__in=extraction_ids,
                        method_id='color_coherence_vector') \
                .values('id', 'directory_path')
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

                image_extractions = ImageExtraction.objects \
                    .filter(extraction_id=extraction['id'],
                            image_name__in=list_of_image_name) \
                    .values('id', 'image_name', 'thumbnail_path')
                image_ids = [item['id'] for item in image_extractions]
                image_extractions = list(image_extractions)
                print("--- Get images: %s seconds ---" % (time.time() - start_time))
                ccv_of_images = ColorCoherenceVector.objects \
                    .filter(image_extraction_id__in=image_ids) \
                    .values('image_extraction_id', 'id', 'alpha', 'beta') \
                    .order_by('id')
                ccv_of_images = list(ccv_of_images)
                print("--- Get CCV: %s seconds ---" % (time.time() - start_time))

                # import django
                # django.setup()

                # faiss
                vector_dict = {}
                vector = []
                for item in ccv_of_images:
                    vector_index = item['image_extraction_id']
                    if vector_index not in vector_dict:
                        vector_dict[vector_index] = []
                    vector_dict[vector_index].append(item['alpha'])
                for key, value in vector_dict.items():
                    vector.append(value)
                vector = np.asarray(vector).astype('float32')
                query = np.asarray([ccv]).astype('float32')

                index = faiss.IndexFlatL2(NUMBER_OF_CCV_COLORS)
                index.add(np.ascontiguousarray(vector))
                distance_array, index_array = index.search(query, 200)
                for i, item in enumerate(index_array[0]):
                    result.append({
                        'image_path': str(os.path.join(directory_path, image_extractions[item]['image_name'])),
                        'thumbnail_path': str(image_extractions[item]['thumbnail_path']),
                        'similarity': str(distance_array[0][i])
                    })

                # For production
                # pool = multiprocessing.Pool(multiprocessing.cpu_count() - 2)
                # result = pool.map(functools.partial(calc_fch_similarity,
                #                                     fch,
                #                                     extraction['directory_path'],
                #                                     fch_of_images,
                #                                     image_extractions), range(0, len(image_extractions), 1))
                # pool.close()
                # pool.join()

                # For local testing
                # result = []
                # for index in range(0, len(image_extractions)):
                #     result.append(calc_ccv_similarity(ccv,
                #                                       extraction['directory_path'],
                #                                       ccv_of_images,
                #                                       image_extractions,
                #                                       index))

                result = list(result)

                result = sorted(result, key=lambda k: k['similarity'])
                print("--- Retrieval: %s seconds ---" % (time.time() - start_time))

                # for index, image in enumerate(image_extractions, start=1):
                #     images_map[image['id']] = calc_fch_similarity(image, fch, extraction, fch_of_images)
                #     print('{}/{}. Degree of similarity ({}): {}'.format(index,
                #                                                         len(list_of_image_name),
                #                                                         image['image_name'],
                #                                                         images_map[image['id']]['similarity']))

            # for key, value in images_map.items():
            #     result.append(value)

        elif method == 'Color Correlogram':
            cc_temp = extract_color_correlogram(-1, colors, 8, 3, 2)
            cc = []
            for key1, value1 in cc_temp.items():
                for key2, value2 in value1.items():
                    cc.append(value2)
            extraction_ids = [5]
            extractions = Extraction.objects \
                .filter(id__in=extraction_ids,
                        method_id='color_correlogram') \
                .values('id', 'directory_path')
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

                image_extractions = ImageExtraction.objects \
                    .filter(extraction_id=extraction['id'],
                            image_name__in=list_of_image_name) \
                    .values('id', 'image_name', 'thumbnail_path')
                image_ids = [item['id'] for item in image_extractions]
                image_extractions = list(image_extractions)
                print("--- Get images: %s seconds ---" % (time.time() - start_time))
                cc_of_images = ColorCorrelogram.objects \
                    .filter(image_extraction_id__in=image_ids) \
                    .values('image_extraction_id', 'id', 'value', 'k') \
                    .order_by('id')
                cc_of_images = list(cc_of_images)
                print("--- Get Color Correlogram: %s seconds ---" % (time.time() - start_time))

                # import django
                # django.setup()

                # faiss
                vector_dict = {}
                vector = []
                for item in cc_of_images:
                    vector_index = item['image_extraction_id']
                    if vector_index not in vector_dict:
                        vector_dict[vector_index] = []
                    vector_dict[vector_index].append(item['value'])
                for key, value in vector_dict.items():
                    vector.append(value)
                vector = np.asarray(vector).astype('float32')
                query = np.asarray([cc]).astype('float32')

                index = faiss.IndexFlatL2(NUMBER_OF_FINE_COLORS)
                index.add(vector)
                distance_array, index_array = index.search(query, 200)
                for i, item in enumerate(index_array[0]):
                    result.append({
                        'image_path': str(os.path.join(directory_path, image_extractions[item]['image_name'])),
                        'thumbnail_path': str(image_extractions[item]['thumbnail_path']),
                        'similarity': str(distance_array[0][i])
                    })

                # For production
                # pool = multiprocessing.Pool(multiprocessing.cpu_count() - 2)
                # result = pool.map(functools.partial(calc_fch_similarity,
                #                                     fch,
                #                                     extraction['directory_path'],
                #                                     fch_of_images,
                #                                     image_extractions), range(0, len(image_extractions), 1))
                # pool.close()
                # pool.join()

                # For local testing
                # result = []
                # for index in range(0, len(image_extractions)):
                #     result.append(calc_cc_similarity(cc,
                #                                      extraction['directory_path'],
                #                                      cc_of_images,
                #                                      image_extractions,
                #                                      index))

                result = list(result)

                result = sorted(result, key=lambda k: k['similarity'])
                print("--- Retrieval: %s seconds ---" % (time.time() - start_time))

                # for index, image in enumerate(image_extractions, start=1):
                #     images_map[image['id']] = calc_fch_similarity(image, fch, extraction, fch_of_images)
                #     print('{}/{}. Degree of similarity ({}): {}'.format(index,
                #                                                         len(list_of_image_name),
                #                                                         image['image_name'],
                #                                                         images_map[image['id']]['similarity']))

            # for key, value in images_map.items():
            #     result.append(value)
        elif method == 'Cumulative Color Histogram':
            extract_cumulative_color_histogram(-1, colorMap)
        return JsonResponse(result, safe=False)
