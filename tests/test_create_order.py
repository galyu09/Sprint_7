import allure
import pytest
from api.orders import OrdersApi


# Utility function to create random string
def create_random_string(length=10):
    import random
    import string
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


# Sample order data for testing
ORDER_WITH_SINGLE_COLOR = {
    "first_name": "Emily",
    "last_name": "Brown",
    "address": "321 Birch St",
    "metro_station": "5",
    "phone": "5551234567",
    "rent_duration": 1,
    "delivery_date": "2024-06-15T18:00:00.000Z",
    "comment": "Sample order",
    "color": ["GREY"]
}

ORDER_WITH_MULTIPLE_COLORS = {
    "first_name": "Michael",
    "last_name": "Taylor",
    "address": "654 Maple St",
    "metro_station": "6",
    "phone": "5559876543",
    "rent_duration": 2,
    "delivery_date": "2024-06-15T18:00:00.000Z",
    "comment": "Sample order",
    "color": ["BLACK", "GREY"]
}

ORDER_WITHOUT_COLOR = {
    "first_name": "Sophia",
    "last_name": "Wilson",
    "address": "789 Cedar St",
    "metro_station": "7",
    "phone": "5556781234",
    "rent_duration": 3,
    "delivery_date": "2024-06-15T18:00:00.000Z",
    "comment": "Sample order"
}


class TestOrderPlacement:
    @allure.title('Успешное размещение заказа')
    @allure.description('Проверяем, что валидный запрос возвращает статус 201 и ьело ответа содержит track.')
    @pytest.mark.parametrize("order_data", [
        ORDER_WITH_SINGLE_COLOR,
        ORDER_WITH_MULTIPLE_COLORS,
        ORDER_WITHOUT_COLOR
    ])
    def test_order_success(self, order_data):
        response = OrdersApi.place_order(order_data)

        assert (response.status_code == 201
                and response.json()['track'] is not None
                and response.json()['track'] > 0)
