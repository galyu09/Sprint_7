import random
import string
import allure
import pytest
from api.couriers import CourierApi





# Helper functions
def generate_random_string_for_test_data(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier_and_return_login_password():
    return (
        generate_random_string_for_test_data(10),
        generate_random_string_for_test_data(10),
        generate_random_string_for_test_data(10)
    )

# Test class
class TestCreateCourier:
    @allure.title('Успешное создание курьера')
    @allure.description('Проверяем, что запрос возвращает валидный код ответа 200 и ожидаемое тело ответа')
    def test_create_courier_success(self, courier):
        response_create_courier = CourierApi.create_courier(courier)

        assert response_create_courier.status_code == 201
        assert response_create_courier.json()['ok'] is True

    @allure.title('Создание дублирующего курьера')
    @allure.description('Проверяем, что запрос вернет код 409 и ожидаемое тело ответа ')
    def test_create_courier_conflict(self, existing_courier):
        CourierApi.create_courier(existing_courier)
        response_create_courier_error = CourierApi.create_courier(existing_courier)

        assert response_create_courier_error.status_code == 409
        assert response_create_courier_error.json()['message'] == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Ошибка запроса на создание заказа без обязательного параметра')
    @allure.description('Проверяем, что запрос без обязательного параметра вернут код 400 и ожидаемое тело ответа')
    @pytest.mark.parametrize("body", [
        {'password': generate_random_string_for_test_data(10), 'firstName': generate_random_string_for_test_data(10)},  # No login
        {'login': "", 'password': generate_random_string_for_test_data(10), 'firstName': generate_random_string_for_test_data(10)},  # Empty login
        {'login': generate_random_string_for_test_data(10), 'firstName': generate_random_string_for_test_data(10)},  # No password
        {'login': generate_random_string_for_test_data(10), 'password': "", 'firstName': generate_random_string_for_test_data(10)}  # Empty password
    ])
    def test_create_courier_bad_request(self, body):
        response_create_courier_bad_request = CourierApi.create_courier(body)

        assert response_create_courier_bad_request.status_code
