import allure
import pytest
import data
from api_test.couriers import CourierApi


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
