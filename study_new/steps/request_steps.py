import requests
from nacl.pwhash.argon2i import verify

# Отправка запроса для получения ответа для метода POST
# url - endpoint
# request - json
def request_post(url, request):
    request = requests.post(url, json=request, verify=False)
    return request

def request_get(url):
    request = requests.get(url, verify=False)
    return request

def request_put(url, request):
    request = requests.put(url, json=request, verify=False)
    return request