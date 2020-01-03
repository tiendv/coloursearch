import os
import cv2
import csv
import json
import math
import time
import collections
import numpy as np
from ..constants import *
from ..views.annotate import *
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..models import Extraction, ImageExtraction, FuzzyColorHistogram
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space


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
            print("--- Histogram: %s seconds ---" % (time.time() - start_time))
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
            for row in colorMap:
                color_row = []
                for color in row:
                    color = list(map(int, color))
                    color_row.append(color)
                colors.append(color_row)
            print("--- Histogram: %s seconds ---" % (time.time() - start_time))
        else:
            return

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
                print("--- Get images: %s seconds ---" % (time.time() - start_time))
                fch_of_images = FuzzyColorHistogram.objects\
                    .filter(image_extraction_id__in=image_ids)\
                    .values('image_extraction_id', 'id', 'value')\
                    .order_by('id')
                print("--- Get FCH: %s seconds ---" % (time.time() - start_time))
                for index, image in enumerate(images, start=1):
                    images_map[image['id']] = {
                        'image_path': os.path.join(extraction['directory_path'], image['image_name']),
                        'thumbnail_path': image['thumbnail_path'],
                        'similarity': 1.0
                    }
                    fch_of_image = [item['value'] for item in fch_of_images if item['image_extraction_id'] == image['id']]
                    # fch_of_image = np.float32(fch_of_image)
                    similarity = 1.0
                    if len(fch) == len(fch_of_image):
                        for i in range(len(fch)):
                            similarity += (fch[i] - fch_of_image[i]) ** 2
                        # similarity = cv2.norm(fch - fch_of_image, cv2.NORM_L2)
                    similarity = math.sqrt(similarity)
                    images_map[image['id']]['similarity'] = similarity
                    print('{}/{}. Degree of similarity ({}): {}'.format(index, len(list_of_image_name), image['image_name'], similarity))
            result = []
            for key, value in images_map.items():
                result.append(value)
            result = sorted(result, key=lambda k: k['similarity'])
            print("--- Retrieval: %s seconds ---" % (time.time() - start_time))
            return JsonResponse(result, safe=False)

        elif method == 'Color Coherence Vector':
            extract_color_coherence_vector(-1, colorMap)
        elif method == 'Color Correlogram':
            extract_color_correlogram(-1, colorMap)
        elif method == 'Cumulative Color Histogram':
            extract_cumulative_color_histogram(-1, colorMap)
        return HttpResponseRedirect('/')
