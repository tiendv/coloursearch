import os
from datetime import datetime
import pytz
from ..models import Extraction, ImageExtraction, Method
from ..utilities.FuzzyColorHistogramExtraction import extract_fuzzy_color_histogram, quantize_color_space
from ..utilities.ColorCoherenceVectorExtraction import extract_color_coherence_vector
from ..utilities.ColorCorrelogramExtraction import extract_color_correlogram
from ..utilities.CumulativeColorHistogramExtraction import extract_cumulative_color_histogram


def extract_features(path, method, param1, param2, param3):
    available_methods = {
        m['name']: m['detail'] for m in Method.objects.all().values()
    }

    if method is None or path is None or method not in available_methods.keys():
        print('You did not include the available method or the directory path. Please re-run the command')
        return
    isNotEnoughParameter = False
    if method == 'fuzzy_color_histogram' or method == 'color_correlogram':
        if param1 is None or param2 is None or param3 is None:
            isNotEnoughParameter = True
    elif method == 'color_coherence_vector':
        if param1 is None or param2 is None:
            isNotEnoughParameter = True
    elif method == 'cumulative_color_histogram':
        if param1 is None:
            isNotEnoughParameter = True
    if isNotEnoughParameter:
        print('Not enough parameters!')
        return

    print('==========================================================================')
    print('Extracting ' + method + ' for ' + path)
    print('==========================================================================')

    extraction = Extraction(method_id=method)
    extraction.directory_path = path
    extraction.start_time = str(datetime.now())
    print(extraction.start_time)

    if method == 'fuzzy_color_histogram':
        extraction.param1_name = 'number_of_coarse_color'
        extraction.param2_name = 'number_of_fine_color'
        extraction.param3_name = 'm'
        extraction.param1_value = param1
        extraction.param2_value = param2
        extraction.param3_value = param3
    elif method == 'color_correlogram':
        extraction.param1_name = 'number_of_color'
        extraction.param2_name = 'd'
        extraction.param3_name = 'increment'
        extraction.param1_value = param1
        extraction.param2_value = param2
        extraction.param3_value = param3
    elif method == 'color_coherence_vector':
        extraction.param1_name = 'number_of_color'
        extraction.param2_name = 'tau'
        extraction.param1_value = param1
        extraction.param2_value = param2
    elif method == 'cumulative_color_histogram':
        extraction.param1_name = 'number_of_color'
        extraction.param1_value = param1
    extraction.save()

    latest_extraction_id = Extraction.objects.latest('id').id

    # r=root, d=directories, f = files
    images = []
    for r, d, f in os.walk(path):
        for file in f:
            if ('.jpg' in file) or ('.png' in file):
                images.append(os.path.join(r, file))

    if method == 'fuzzy_color_histogram':
        number_of_coarse_color = param1
        number_of_fine_color = param2
        m = param3
        coarse_color_range, coarse_channel_range, matrix, v = quantize_color_space(number_of_coarse_color,
                                                                                number_of_fine_color, m)
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('extraction_id').extraction_id
            print(latest_extraction_id)
            print(img_extraction_id)
            extract_fuzzy_color_histogram(img_extraction_id, img, coarse_color_range, coarse_channel_range, matrix, v)
    elif method == 'color_coherence_vector':
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('extraction_id').extraction_id
            extract_color_coherence_vector(img_extraction_id, img, param1, param2)
    elif method == 'color_correlogram':
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('extraction_id').extraction_id
            extract_color_correlogram(img_extraction_id, img, param1, param2, param3)
    elif method == 'cumulative_color_histogram':
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('extraction_id').extraction_id
            extract_cumulative_color_histogram(img_extraction_id, img, param1)

    latest_extraction = Extraction.objects.latest('id')
    latest_extraction.end_time = str(datetime.now())
    latest_extraction.save()

    print('|------------------|')
    print('| Extraction done. |')
    print('|------------------|')

    return True
