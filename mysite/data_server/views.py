from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SoundData

import requests, json,datetime
import hashlib

json_error_response = JsonResponse({'status': '500'})
# Create your views here.


@csrf_exempt
def handle_sound_data_list(request):
    print(request.body)
    if request.method == 'POST':
        response = parse_data_packages(request)
        return response

    return json_error_response


def parse_data_packages(request):
    received_data = request.body.decode('utf-8')
    print("Received: ")
    print(received_data)
    received_data_lists = json.loads(received_data)
    for sound_data in received_data_lists:
        save_sound_data(sound_data)

    return JsonResponse({'status': '200'})

def save_sound_data(received_data):
    req_date = datetime.datetime.strptime(received_data['time'],"%Y-%m-%d %H:%M:%S.%f")

    data = SoundData(dB=received_data['dB'], time=req_date, photoId=received_data['photoId'])

    sha_256 = hashlib.sha256()

    if SoundData.objects.last() is None:
        sha_256.update(bytes(str(data.time)+ str(data.dB),'UTF-8'))
    else:
        sha_256.update(bytes(str(data.time)+ str(data.dB),'UTF-8') + SoundData.objects.last().hash)

    data.hash = sha_256.digest()

    print("Data: ")
    print(data)

    data.save()


def send_sound_data_list(data):
    url = 'Firebase'
    requests.post(url=url, data=data)


def send_push():
    url = 'Firebase'
    data = dict({
        'message' : 'message'
    })
    requests.post(url=url, data=data)