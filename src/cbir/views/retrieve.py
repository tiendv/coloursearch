import os
from datetime import datetime
from ..models import Extraction, ImageExtraction, Method
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram
from django.shortcuts import render
import json
from django.http import HttpResponseRedirect


def retrieve(request):
    if request.method == 'POST':
        colorMap = json.loads(request.POST.get('colorMap'))
        method = request.POST.get('method')
        print(colorMap)
        print(method)

        if method == 'Fuzzy Color Histogram':
            matrix_path = os.path.join(settings.BASE_DIR, 'matrix')

            coarse_color_range, coarse_channel_range, matrix, v = quantize_color_space()
            extract_fuzzy_color_histogram(-1, colorMap, coarse_color_range, coarse_channel_range, matrix, v)
        elif method == 'Color Coherence Vector':
            extract_color_coherence_vector(-1, colorMap)
        elif method == 'Color Correlogram':
            extract_color_correlogram(-1, colorMap)
        elif method == 'Cumulative Color Histogram':
            extract_cumulative_color_histogram(-1, colorMap)

        return HttpResponseRedirect('/')
