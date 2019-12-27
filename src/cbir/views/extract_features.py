import os
import cv2
import time
from ..constants import *
from django.conf import settings
from datetime import datetime
from ..utilities.Utilities import image_resize
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
    print("Extraction started at " + str(extraction.start_time))

    if method == 'fuzzy_color_histogram':
        extraction.param1_name = 'number_of_coarse_colors'
        extraction.param2_name = 'number_of_fine_colors'
        extraction.param3_name = 'm'
        extraction.param1_value = param1
        extraction.param2_value = param2
        extraction.param3_value = param3
    elif method == 'color_correlogram':
        extraction.param1_name = 'number_of_colors'
        extraction.param2_name = 'd'
        extraction.param3_name = 'increment'
        extraction.param1_value = param1
        extraction.param2_value = param2
        extraction.param3_value = param3
    elif method == 'color_coherence_vector':
        extraction.param1_name = 'number_of_colors'
        extraction.param2_name = 'tau'
        extraction.param1_value = param1
        extraction.param2_value = param2
    elif method == 'cumulative_color_histogram':
        extraction.param1_name = 'number_of_colors'
        extraction.param1_value = param1
    extraction.save()

    latest_extraction_id = Extraction.objects.latest('id').id
    thumbnail_path = os.path.join(settings.BASE_DIR, 'static', 'thumbnails', str(latest_extraction_id))
    if not os.path.exists(thumbnail_path):
        os.makedirs(thumbnail_path)

    # r=root, d=directories, f = files
    images = []
    for r, d, f in os.walk(path):
        for file in f:
            if ('.jpg' in file) or ('.png' in file) or ('.tif' in file):
                images.append(os.path.join(r, file))

    if method == 'fuzzy_color_histogram':
        number_of_coarse_colors = param1
        number_of_fine_colors = param2
        m = param3
        coarse_color_ranges, coarse_channel_ranges, matrix, v = quantize_color_space(number_of_coarse_colors,
                                                                                number_of_fine_colors, m)
        for img in images:
            image_name = os.path.basename(img)
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = image_name
            image_thumbnail_path = os.path.join('static', 'thumbnails', str(latest_extraction_id), image_name)
            img_extraction.thumbnail_path = image_thumbnail_path
            img_extraction.save()

            # Save thumbnail
            thumbnail = cv2.imread(img)
            thumbnail = image_resize(thumbnail, height=THUMBNAIL_IMAGE_HEIGHT)
            cv2.imwrite(image_thumbnail_path, thumbnail)
            print('Saved thumbnail for {} in {}'.format(image_name, image_thumbnail_path))

            img_extraction_id = ImageExtraction.objects.latest('id').id
            extract_fuzzy_color_histogram(img_extraction_id, img, coarse_color_ranges, coarse_channel_ranges, matrix, v)

    elif method == 'color_coherence_vector':
        for img in images:
            image_name = os.path.basename(img)
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            image_thumbnail_path = os.path.join('static', 'thumbnails', str(latest_extraction_id), image_name)
            img_extraction.thumbnail_path = image_thumbnail_path
            img_extraction.save()

            # Save thumbnail
            thumbnail = cv2.imread(img)
            thumbnail = image_resize(thumbnail, height=THUMBNAIL_IMAGE_HEIGHT)
            cv2.imwrite(image_thumbnail_path, thumbnail)
            print('Saved thumbnail for {} in {}'.format(image_name, image_thumbnail_path))

            img_extraction_id = ImageExtraction.objects.latest('id').id
            extract_color_coherence_vector(img_extraction_id, img, param1, param2)

    elif method == 'color_correlogram':
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('id').id
            extract_color_correlogram(img_extraction_id, img, param1, param2, param3)
    elif method == 'cumulative_color_histogram':
        for img in images:
            img_extraction = ImageExtraction(extraction_id=latest_extraction_id)
            img_extraction.image_name = os.path.basename(img)
            img_extraction.save()
            img_extraction_id = ImageExtraction.objects.latest('id').id
            extract_cumulative_color_histogram(img_extraction_id, img, param1)

    latest_extraction = Extraction.objects.latest('id')
    latest_extraction.end_time = str(datetime.now())
    latest_extraction.save()

    print('|------------------|')
    print('| Extraction done. |')
    print('|------------------|')

    return True
