from django.http import JsonResponse
from ..models.Extraction import *


def get_extractions(request):
    extractions = list(Extraction.objects.values())
    return JsonResponse(extractions, safe=False)
