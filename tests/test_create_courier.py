import random
import string
import allure
import pytest
import requests
from api.couriers import CourierApi
from api.urls import Urls
import data

# метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post(Urls.CREATE_COURIER, data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass


class TestCreateCourier:
    @allure.title('Успешное создание курьера')
    @allure.description('Проверяем, что запрос возвращает валидный код ответа 200 и ожидаемое тело ответа')
    def test_create_courier_positive(self, courier):
        response_create_courier = CourierApi.create_courier(courier)
        assert response_create_courier.status_code == 201
        assert response_create_courier.json()['ok'] is True

    @allure.title('Создание дублирующего курьера')
    @allure.description('Проверяем, что запрос вернет код 409 и ожидаемое тело ответа ')
    def test_create_double_courier_error(self, courier):
        response_create_courier = CourierApi.create_courier(courier)
        assert response_create_courier.status_code == 201
        response_create_courier_error = CourierApi.create_courier(courier)
        assert response_create_courier_error.status_code == 409
        assert response_create_courier_error.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Ошибка запроса на создание заказа без обязательного параметра')
    @allure.description('Проверяем, что запрос без обязательного параметра вернут код 400 и ожидаемое тело ответа')
    @pytest.mark.parametrize(
        'payload',
        (
            pytest.param(data.COURIER_EMPTY_LOGIN, id='empty_login'),
            pytest.param(data.COURIER_WITHOUT_LOGIN, id='without_login'),
            pytest.param(data.COURIER_WITHOUT_PASSWORD, id='without_password'),
            pytest.param(data.COURIER_EMPTY_PASSWORD, id='empty_password')
        ),
    )
    def test_create_courier_without_required_field(self, payload):
        response_create_courier_bad_request = CourierApi.create_courier(payload)
        assert response_create_courier_bad_request.status_code == 400
        assert response_create_courier_bad_request.json()['message'] == "Недостаточно данных для создания учетной записи"
