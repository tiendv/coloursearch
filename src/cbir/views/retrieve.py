import os
import math
import numpy as np
from datetime import datetime
from ..models import Extraction, ImageExtraction, Method, FuzzyColorHistogram
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from django.shortcuts import render
from ..utilities.FuzzyColorHistogramExtraction import calc_color_range, extract_rgb_color_histogram
from ..models.FuzzyColorHistogramColor import FuzzyColorHistogramColor
import csv
import json
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse


def retrieve(request):
    if request.method == 'POST':
        colors = []
        colorMap = json.loads(request.POST.get('colorMap'))
        for row in colorMap:
            color_row = []
            for color in row:
                color = list(map(int, color[4:-1].replace(' ', '').split(',')))
                color_row.append(color)
            colors.append(color_row)
        method = request.POST.get('method')
        print(colorMap)
        print(method)

        if method == 'Fuzzy Color Histogram':
            number_of_coarse_colors = 4096
            number_of_fine_colors = 64
            m = 1.9
            matrix_path = os.path.join(settings.BASE_DIR, 'matrix')
            csv_file = ''
            for r, d, f in os.walk(matrix_path):
                for file in f:
                    if '.csv' in file:
                        file_name = os.path.splitext(file)[0]
                        if file_name == '4096_64':
                            csv_file = os.path.join(r, file)
            print(csv_file)
            if csv_file == '':
                coarse_color_ranges, coarse_channel_ranges, matrix, v = quantize_color_space()
            else:
                v = FuzzyColorHistogramColor.objects\
                    .filter(number_of_coarse_colors=4096, number_of_fine_colors=64)\
                    .values('ccomponent1', 'ccomponent2', 'ccomponent3')
                v = [[item['ccomponent1'], item['ccomponent2'], item['ccomponent3']] for item in v]
                with open(csv_file) as csv_file:
                    csv_reader = csv.reader(csv_file, quoting=csv.QUOTE_ALL)
                    matrix = list(csv_reader)
                coarse_color_ranges, coarse_colors, coarse_channel_ranges = calc_color_range(4096)
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
                for image in images:
                    images_map[image['id']] = {
                        'image_path': os.path.join(extraction['directory_path'], image['image_name']),
                        'thumbnail_path': image['thumbnail_path'],
                        'similarity': 0.0
                    }
                    fch_of_image = FuzzyColorHistogram.objects\
                        .filter(image_extraction_id=image['id'])\
                        .values('id', 'value')\
                        .order_by('id')
                    fch_of_image = [item['value'] for item in fch_of_image]
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
