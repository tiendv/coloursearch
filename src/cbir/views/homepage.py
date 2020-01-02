from datetime import datetime
from django.shortcuts import render
from ..models.Extraction import Extraction


def homepage(request, *args, **kwargs):
    print(request.user)
    extractions = Extraction.objects.all()
    extractions = list(extractions)
    for extraction in extractions:
        if extraction.start_time is not None:
            extraction.start_time = datetime \
                .strptime(extraction.start_time, '%Y-%m-%d %H:%M:%S.%f') \
                .strftime('%Y-%m-%d %H:%M:%S')
        if extraction.end_time is not None:
            extraction.end_time = datetime \
                .strptime(extraction.end_time, '%Y-%m-%d %H:%M:%S.%f') \
                .strftime('%Y-%m-%d %H:%M:%S')
    context = {
        'extractions': extractions
    }
    return render(request, 'html/homepage.html', context)
