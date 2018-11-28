from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
# from scraping_project.main import run_scrapy
import os
import json

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        folder='web_server/scraping_project/'
        myfile = request.FILES['file']
        fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT
        filename = fs.save('project_website_list.csv', myfile)
        file_url = fs.url(filename)
        form = UploadFileForm()
        #run_scrapy()
        return render(request, 'upload.html', {
            'state': 'upload success',
            'form': form
        })
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {
        'form': form,
    })

def handle_uploaded_file(f):
    print('handle_uploaded_file')
