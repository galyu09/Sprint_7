import allure
import pytest
from api.couriers import CourierApi
from tests import data


@allure.suite('Тесты авторизации')
class TestCourierAuthentication:
    @allure.title('Залогин курьером с валидными данными')
    @allure.description(
        'Проверяем, что валидный запрос на логин существующего курьера возвращает код 200 и id в теле ответа')
    def test_courier_login_success(self):
        payload = data.COURIER_DATA_VALID
        CourierApi.create_courier(payload)
        response = CourierApi.login_courier(payload)
        courier_id = response.json()['id']
        assert response.status_code == 200
        assert courier_id is not None
        assert courier_id > 0
        CourierApi.delete_courier(courier_id)

    @allure.title('Запрос на авторизацию несуществующим курьером')
    @allure.description(
        'Проверяем, что запрос на вход несуществующим курьером вернет код 404 и ожидаемым текстом в теле ответа')
    def test_courier_not_found(self):
        response = CourierApi.login_courier(data.COURIER_DATA_VALID)
        assert response.status_code == 404
        assert response.json()['message'] == 'Учетная запись не найдена'

    @allure.title('Запрос на логин без обязательного параметра')
    @allure.description(
        'Проверяем, что запрос на логин без обязательного параметра вернет код 400 и ожидаемым текстом в теле ответа')
    @pytest.mark.parametrize(
        'payload',
        (
            pytest.param(data.COURIER_EMPTY_LOGIN, id='empty_login'),
            pytest.param(data.COURIER_WITHOUT_LOGIN, id='without_login'),
            pytest.param(data.COURIER_WITHOUT_PASSWORD, id='without_password'),
            pytest.param(data.COURIER_EMPTY_PASSWORD, id='empty_password')
        ),
    )
    @pytest.mark.parametrize(
        'should_create_courier',
        (
            pytest.param(True, id='courier_exists'),
            pytest.param(False, id='courier_doesnt_exists')
        ),
    )
    def test_courier_login_bad_request(self, payload, should_create_courier):
        if should_create_courier:
            CourierApi.create_courier(payload)
        response = CourierApi.login_courier(payload)
        assert response.status_code == 400
        assert response.json()['message'] == 'Недостаточно данных для входа'
        if should_create_courier:
            CourierApi.delete_courier_by_payload(payload)