from django.shortcuts import render
from django.http import JsonResponse
import multiprocessing

from .constants import SELECT_CATEGORIES, SELECT_CITIES, REMOTE_CATETORIES, REMOTE_CITIES

from .modules.subito import subitoProc

processor = None
# Create your views here.
def home(request):
    data = {}
    data['remove_cities'] = REMOTE_CITIES
    data['remote_categories'] = REMOTE_CATETORIES
    data['select_categories'] = SELECT_CATEGORIES
    data['select_cities'] = SELECT_CITIES
    return render(request, 'home.html', data)

def scraping(request):
    global processor
    if request.POST.get('is_start') == 'true':
        if not processor or not processor.is_alive():
            print('-' * 30, ' processing ', '-' * 30)
            processor = multiprocessing.Process(target=subitoProc, args=(request.POST,))
            processor.start()
    else:
        if processor:
            print('-' * 30, ' terminated ', '-' * 30)
            processor.terminate()

    return JsonResponse({'success': True})