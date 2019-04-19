from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import os
import json
import datetime

@csrf_exempt
def enter_face(request):
    print(request.FILES['media'])
    myfile = request.FILES['media']
    fs = FileSystemStorage()
    filename = fs.save("temp/"+myfile.name, myfile)
    file_url = fs.url(filename)
    print(file_url)
    return HttpResponse('Success', status=200)
