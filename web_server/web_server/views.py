from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from web_server.scraping_project.start_scrapy import run_spider
import os
import json
import datetime

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        folder='web_server/scraping_project/'
        myfile = request.FILES['file']
        level = request.POST.get('level')
        fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
        fs.delete('project_website_list.csv')
        filename = fs.save('project_website_list.csv', myfile)
        file_url = fs.url(filename)
        form = UploadFileForm()
        run_spider(level)
        return render(request, 'upload.html', {
            'state': 'upload success',
            'form': form
        })
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form,
    })

def search(request):
    state = 'searching'
    return render(request, 'search.html', {
        'state': state,
    })

@csrf_exempt
def enter_face(request):
    print(request.FILES['media'])
    myfile = request.FILES['media']
    fs = FileSystemStorage()
    filename = fs.save("temp/"+myfile.name, myfile)
    file_url = fs.url(filename)
    print(file_url)
    return HttpResponse('Success', status=200)
