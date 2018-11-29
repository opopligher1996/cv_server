from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from web_server.scraping_project.start_scrapy import run_spider
import os
import json

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
        print('start_scrapy')
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
