import allure
import pytest
from api.orders import OrdersApi
from tests import data


# Генерим строку для логина/пароля/имени
def create_random_string(length=10):
    import random
    import string
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


class TestOrderPlacement:
    @allure.title('Успешное размещение заказа')
    @allure.description('Проверяем, что валидный запрос возвращает статус 201 и тело ответа содержит track.')
    @pytest.mark.parametrize(
        'order_data',
        (
            pytest.param(data.ORDER_WITH_SINGLE_COLOR, id='single_color'),
            pytest.param(data.ORDER_WITH_MULTIPLE_COLORS, id='multiply_color'),
            pytest.param(data.ORDER_WITHOUT_COLOR, id='without_color')
        ),
    )
    def test_order_success(self, order_data):
        response = OrdersApi.place_order(order_data)

        assert (response.status_code == 201
                and response.json()['track'] is not None
                and response.json()['track'] > 0)
