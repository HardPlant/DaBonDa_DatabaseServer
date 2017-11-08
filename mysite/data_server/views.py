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
        return parse_data_packages(request)
    if request.method == 'GET':
        return get_data_packages(request)

    return json_error_response


def get_data_packages(request):
    if request.GET.get('to_date') is None \
        or request.GET.get('from-date') is None:
        return json_error_response

    to_date = request.GET.get('to_date')
    from_date = request.GET.get('from-date')
    res = []
    data_list = SoundData.objects.filter(time__range=[from_date, to_date])

    for item in data_list:
        cur_dB = item['dB']
        cur_time = str(item['time'])
        res.append(json.dumps({'dB' : cur_dB,
                               'time' : cur_time}))

    return JsonResponse(json.dumps(res))


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

def verify_sound_data(from_pk, to_pk):
    assert(from_pk <= to_pk)

    from_data = SoundData.objects.get(pk=from_pk)
    to_data = SoundData.objects.get(pk=to_pk)
    hash = from_data.hash

    for i in range(from_pk+1,to_pk+1):
        sha_256 = hashlib.sha256()
        current_dB = SoundData.objects.get(i).dB
        current_time = SoundData.objects.get(i).time
        hash = sha_256.update(bytes(str(current_time)+ str(current_dB),'UTF-8')
                              + hash)

    if hash == to_data.hash:
        return True
    else:
        return False

def send_sound_data_list(data):
    url = 'Firebase'
    requests.post(url=url, data=data)

def send_push():
    url = 'Firebase'
    data = dict({
        'message' : 'message'
    })
    requests.post(url=url, data=data)