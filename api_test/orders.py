import allure
import pytest
import requests
from tests.urls import *


class OrdersApi:
    @staticmethod
    @allure.step('Отправка запроса на создание заказа')
    def place_order(body):
        response = requests.post(Urls.PLACE_ORDER, json=body)
        return response

    @staticmethod
    @allure.step('Отправка запроса на получение списка заказов')
    def fetch_order_list():
        response = requests.get(Urls.FETCH_ORDERS)
        return response
