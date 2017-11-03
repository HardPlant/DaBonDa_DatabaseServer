from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SoundData

import requests, json,datetime
json_error_response = JsonResponse({'status': '500'})
# Create your views here.
@csrf_exempt

def sound_data(request):
    print(request.body)
    if request.method == 'POST':
        response = post_sound_data(request)
        return response

    return json_error_response

def post_sound_data(request):
    received_data = request.body.decode('utf-8')
    print("Received: ")
    print(received_data)
    received_data = json.loads(received_data)
    req_date = datetime.datetime.strptime(received_data['time'],"%Y-%m-%d %H:%M:%S.%f")

    data = SoundData(dB=received_data['dB'], time=req_date, photoId=received_data['photoId'])
    print("Data: ")
    print(data)

    data.save()

    return JsonResponse({'status': '200'})


def send_sound_data_list(data):
    url = 'Firebase'
    requests.post(url=url, data=data)

def send_push():
    url = 'Firebase'
    data = dict({
        'message' : 'message'
    })
    requests.post(url=url, data=data)