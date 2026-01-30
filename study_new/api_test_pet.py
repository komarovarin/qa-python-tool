import pytest
import requests
from nacl.pwhash.argon2i import verify

import resourse.urls as urls
from steps import support_steps as support_steps
from steps import generate_jsin_steps as generate_json_steps
from steps import request_steps as request_steps
from steps import assert_steps as assert_steps

# Тест создания нового питомца
@pytest.mark.smoke_test
@pytest.mark.regress_test
@pytest.mark.parametrize(
    'type',
    [
        (generate_json_steps.create_json_post_pet_required_params()),
        (generate_json_steps.create_json_post_pet_all_params())
    ],
    ids = ['required params', 'all params']
)
def test_post_pet(type):
#Создание нового питомца JSON с передаваемым типом
    request = type
# отправка запроса
    request_post = request_steps.request_post(urls.url_pet_post, request)
    print('result =', request_post.json())
    pet_id = request_post.json()['id']
#Проверка непустого ответа
    assert_steps.assert_not_none_id(request_post)
#Проверка через get что запрос создан
    request_get = request_steps.request_get(urls.url_pet_get(str(request_post.json()['id'])))
    print('request_get =', request_get)

# Проверка, что по данному ID возвращается первоначально созданный объект
    print(request_post.json()['id'])
    print(request_get.json())
    # assert request_post.json()['id'] == request_get.json()['id']
    # assert_steps.assert_equals_response_ids(request_post, request_get)

def test_post_name_negative():
    # создаем json c для создания питомца
    request = create_request_json.generate_json_pet()
    # заменяем в нем имя категории на невалидное
    request["category"]["name"] = []
    # отправляем запрос
    response_post = requests_steps.request_post(urls.url_pet_post, request)
    print("result =", response_post.json())
    # проверяем ответ
    assert_steps.assert_equals_response_values(response_post.json()['message'],"something bad happened")

def test_post_negative_pet():
    request = type
    print('request =', request)

    response_post = requests.post(urls.url_pet_post, json=request)
    print('result =', response_post.json())

    assert response_post.json()['message'] == 'something bad happened'

def test_get_pet():
    url = f'https://petstore.swagger.io/v2/pet/'
    requests_get = requests.get(url, verify=False)
    print('result_get =', requests_get.json())

    # assert str(requests_get.json()['id']) == '9223372036854754819'

def test_get_negative_pet():
    requests_get = requests.get(urls.url_pet_post, verify=False)
    print('result_get =', requests_get.json())

    assert requests_get.json()['message'] == 'Pet not found'

@pytest.mark.regress_test
@pytest.mark.parametrize(
    'type',
    [
        (generate_json_steps.create_json_post_pet_required_params()),
        (generate_json_steps.create_json_post_pet_all_params())
    ],
    ids=['required params', 'all params']
)
def test_put_pet(type):
    #отправляем POST запрос
    request = type
    print('request =', request)
    # Получаем тело запроса
    request_post = request_steps.request_post(urls.url_pet_post, request)
    print("result post =", request_post.json())

    # Отправляем PUT запрос с новыми данными
    request_put = type
    print('request put =', request_put)

    request_put_r = requests.put(urls.url_pet_post, json=request, verify=False)
    print('result put r =', request_put_r)

    assert request_put_r.json()['name'] == request_put['name']

    # url_get = "https://petstore.swagger.io/v2/pet/" + str(request_post.json()['id'])
    # request_get = requests.get(urls.url_pet_post_uploadimage, verify=False)
    #
    # assert request_get.json()['massage'] == 'something bad happened'

def test_put_negative_pet():
    url = "https://petstore.swagger.io/v2/pet"

    request_put = {}
    request_put ['id'] = []
    request_put ['name'] = 'sberdog'
    request_put ['photoUrls'] = ['photosberDog']
    print('request put =', request_put)

    request_put_r = requests.put(url, json=request_put, verify=False)
    print('result put r =', request_put_r.json())

def test_delete_pet():
    url = "https://petstore.swagger.io/v2/pet"
    request = {}
    request ['id'] = '12345'
    request ['name'] = 'sbercat'
    request ['photoUrls'] = ['photosberCat']
    request ['category'] = {}
    request ['category'] ['name'] = 'cats'
    print('request =', request)

    request_post = requests.post(url, json=request)
    print('result =', request_post.json())

    url_delete = 'https://petstore.swagger.io/v2/pet/' + str(request_post.json()['id'])
    print('url_delete', url_delete)

    request_delete = requests.delete(url_delete)
    print('result delete =', request_delete)

    assert request_delete.json()['code'] == 200

    request_get = requests.get(url_delete, verify=False)
    assert request_get.json()['message'] == 'Pet not found'

def test_delete_negative_pet():
    url_delete = 'https://petstore.swagger.io/v2/pet/' + '777777777'

    request_delete = requests.delete(url_delete, verify=False)
    print("result delete =", request_delete)

    assert str(request_delete).__contains__('404')