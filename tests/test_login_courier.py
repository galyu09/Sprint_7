import allure
import pytest
from api.couriers import CourierApi

# Примеры данных для курьерских запросов
COURIER_DATA_VALID = {
    'login': 'valid_courier',
    'password': 'valid_password'
}

COURIER_DATA_NOT_FOUND = {
    'login': 'not_found',
    'password': 'any_password'
}

COURIER_DATA_MISSING_LOGIN = {
    'password': 'some_password'
}

COURIER_DATA_EMPTY_LOGIN = {
    'login': '',
    'password': 'some_password'
}

COURIER_DATA_EMPTY_PASSWORD = {
    'login': 'some_login',
    'password': ''
}
@allure.suite('Тесты авторизации')
class TestCourierAuthentication:
    @allure.title('Successful courier login.')
    @allure.description('Verify successful courier login returns status 200 and a valid ID in the response body.')
    def test_courier_login_success(self):
        CourierApi.create_courier(COURIER_DATA_VALID)
        response = CourierApi.login_courier(COURIER_DATA_VALID)
        courier_id = response.json()['id']

        assert response.status_code == 200
        assert courier_id is not None
        assert courier_id > 0

    @allure.title('Запрос на авторизацию несуществующим курьером')
    @allure.description('Проверяем, что запрос на вход несуществующим курьером вернет код 404 и ожидаемым текстом в теле ответа')
    def test_courier_not_found(self):
        response = CourierApi.login_courier(COURIER_DATA_NOT_FOUND)

        assert response.status_code == 404
        assert response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Запрос на логин без обязательного параметра')
    @allure.description('Проверяем, что запрос на логин без обязательного параметра вернет код 400 и ожидаемым текстом в теле ответа')
    @pytest.mark.parametrize("body", [COURIER_DATA_MISSING_LOGIN,
                                      COURIER_DATA_EMPTY_LOGIN,
                                      COURIER_DATA_EMPTY_PASSWORD])
    def test_courier_login_bad_request(self, body):
        response = CourierApi.login_courier(body)

        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для входа'
