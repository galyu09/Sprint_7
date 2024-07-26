import allure
import requests
from api.config import *


class CourierApi:
    @staticmethod
    @allure.step("Create courier")
    def create_courier(body):
        response = requests.post(Urls.CREATE_COURIER, json=body)
        return response

    @staticmethod
    @allure.step("Login courier")
    def login_courier(body):
        response = requests.post(Urls.LOGIN_COURIER, json=body)
        return response

    @staticmethod
    @allure.step("Delete courier")
    def delete_courier(courier_id):
        response = requests.delete(f"{Urls.DELETE_COURIER}/{courier_id}")
        return response

    @staticmethod
    @allure.step("Create order")
    def create_order(body):
        response = requests.post(Urls.PLACE_ORDER, json=body)
        return response

    @staticmethod
    @allure.step("Get orders")
    def get_orders():
        response = requests.get(Urls.GET_ORDERS)
        return response
    
class CourierApiT:
    @classmethod
    def create_courier(cls, data):
        if not data.get('login') or not data.get('password'):
            return cls.MockResponse(400, {'message': "Insufficient data to create an account"})
        
        if data in cls.existing_couriers:
            return cls.MockResponse(409, {'message': "This login is already in use. Try another one."})
        
        cls.existing_couriers.append(data)
        return cls.MockResponse(201, {'ok': True})


    @staticmethod
    def register_courier(data):
        # Mocked method to simulate courier registration
        return CourierApi.MockResponse(201, {'id': 1})

    @staticmethod
    def authenticate_courier(data):
        if data.get('login') == 'not_found':
            return CourierApi.MockResponse(404, {'message': 'Courier not found'})
        elif not data.get('login') or not data.get('password'):
            return CourierApi.MockResponse(400, {'message': 'Invalid login credentials'})
        else:
            return CourierApi.MockResponse(200, {'id': 12345})

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def json(self):
            return self.json_data