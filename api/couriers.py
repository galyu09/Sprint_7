import allure
import requests
from api.urls import *


class CourierApi:
    @staticmethod
    @allure.step('Создаем курьера')
    def create_courier(payload):
        response = requests.post(Urls.CREATE_COURIER, json=payload)
        return response

    @staticmethod
    @allure.step('Логин курьером')
    def login_courier(payload):
        response = requests.post(Urls.LOGIN_COURIER, json=payload)
        return response

    @staticmethod
    @allure.step('Удаляем курьера')
    def delete_courier(courier_id):
        response = requests.delete(f'{Urls.DELETE_COURIER}/{courier_id}')
        return response
    @staticmethod
    def delete_courier_by_payload(payload):
        login_response = CourierApi.login_courier(payload)
        if login_response.status_code == 200:
            courier_id = login_response.json()['id']
            CourierApi.delete_courier(courier_id)
