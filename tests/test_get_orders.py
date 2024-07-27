import allure
from api.orders import OrdersApi


class TestOrderRetrieval:
    @allure.title('Получение списка заказов')
    @allure.description('Проверяем, что тело ответа содержит список заказов')
    def test_fetch_order_list(self):
        response = OrdersApi.fetch_order_list()
        assert (response.status_code == 200
                and response.json()['orders'] is not None)
