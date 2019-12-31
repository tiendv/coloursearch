import os
import cv2
import csv
import json
import math
import numpy as np
from ..constants import *
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..models import Extraction, ImageExtraction, Method, FuzzyColorHistogram
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space


def retrieve(request):
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
        elif len(request.FILES) > 0:
            image = request.FILES['image']
            colorMap = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            colorMap = cv2.cvtColor(colorMap, cv2.COLOR_BGR2RGB)
            for row in colorMap:
                color_row = []
                for color in row:
                    color = list(map(int, color))
                    color_row.append(color)
                colors.append(color_row)
        else:
            return
        method = request.POST.get('method')
        print(method)

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
            images_map = {}
            extraction_id = [1]
            extractions = Extraction.objects\
                .filter(id__in=extraction_id,
                        param1_value=number_of_coarse_colors,
                        param2_value=number_of_fine_colors,
                        param3_value=m)\
                .values('id', 'directory_path')
            for extraction in extractions:
                images = ImageExtraction.objects\
                    .filter(extraction_id=extraction['id'])\
                    .values('id', 'image_name', 'thumbnail_path')
                image_ids = [item['id'] for item in images]
                fch_of_images = FuzzyColorHistogram.objects\
                    .filter(image_extraction_id__in=image_ids)\
                    .values('image_extraction_id', 'id', 'value')\
                    .order_by('id')
                for image in images:
                    images_map[image['id']] = {
                        'image_path': os.path.join(extraction['directory_path'], image['image_name']),
                        'thumbnail_path': image['thumbnail_path'],
                        'similarity': 0.0
                    }
                    fch_of_image = [item['value'] for item in fch_of_images if item['image_extraction_id'] == image['id']]
                    similarity = 0.0
                    if len(fch) == len(fch_of_image):
                        for i in range(len(fch)):
                            similarity += (fch[i] - fch_of_image[i])**2
                    similarity = math.sqrt(similarity)
                    images_map[image['id']]['similarity'] = similarity
            result = []
            for key, value in images_map.items():
                result.append(value)
            result = sorted(result, key=lambda k: k['similarity'])
            print(images_map)
            return JsonResponse(result, safe=False)

        elif method == 'Color Coherence Vector':
            extract_color_coherence_vector(-1, colorMap)
        elif method == 'Color Correlogram':
            extract_color_correlogram(-1, colorMap)
        elif method == 'Cumulative Color Histogram':
            extract_cumulative_color_histogram(-1, colorMap)

        return HttpResponseRedirect('/')
