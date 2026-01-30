import pytest
import requests
import json
from resourse import urls as urls
from steps import support_steps as support_steps
from nacl.pwhash.argon2i import verify
from requests import request


def test_post_user():
    request = {}
    request ['id'] = '123'
    request ['username'] = support_steps.generate_random_letter_str(6)
    request ['lastname'] = support_steps.generate_random_letter_str(6)
    request ['phone'] = support_steps.generate_random_phone_number(9)
    request ['email'] = 'koma@mail.ru'
    print('request =', request)

    request_post = requests.post(urls.url_user_post, json=request)
    print('result =', request_post.json())

def test_get_user():
    url = 'https://petstore.swagger.io/v2/user/123'
    requests_get = requests.get(url, verify=False)
    print('result =', requests_get.json())

def test_put_user():
    url = 'https://petstore.swagger.io/v2/user'
    request = {}
    request ['username'] = 'arina'
    request ['lastname'] = 'komarova'
    request ['email'] = 'koma@mail.ru'
    print('request =', request)

    request_post = requests.post(url, json=request, verify=False)
    print("result post =", request_post.json())

    request_put ={}
    request_put ['message'] = str(request_post.json()['message'])
    request_put ['username'] = 'Masha'
    request_put ['lastname'] = 'tarzan'
    request_put ['email'] = 'tulin@gmai.com'
    print('request put =', request_put)

    request_put_r = requests.put(url, json=request_put, verify=False)
    print('result put r =', request_put_r)

    assert str(request_put_r).__contains__('405')

def test_delete_user():
    url = 'https://petstore.swagger.io/v2/user'
    request = {}
    # request ['id'] = '123'
    request ['username'] = 'arina'
    request ['lastname'] = 'komarova'
    request ['email'] = 'koma@mail.ru'
    print('request =', request)

    request_post = requests.post(url, json=request)
    print('result =', request_post.json())

    url_delete = 'https://petstore.swagger.io/v2/user/' + str(request_post.json()['message'])
    print('url_delete =', url_delete)

    request_delete = requests.delete(url_delete)
    print('result delete =', request_delete)

    # assert str(request_delete).__contains__('404')
    assert request_delete.json()['code'] == 200

