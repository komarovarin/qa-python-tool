
# ФУНКЦИЯ ПРОВЕРЯЕТ УТВЕРЖДЕНИЕ ЧТО Id не пустой
def assert_not_none_id(request):
    assert request.json()['id'] is not None

# Функция проверяет утверждение что ID запросов равны
def assert_equals_response_ids(first, second):
    assert first.json()['id'] == second.json()['id']
