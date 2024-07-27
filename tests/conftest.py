import pytest

from tests.test_create_courier import register_new_courier_and_return_login_password, generate_random_string


@pytest.fixture
def courier():
    return {
        'login': generate_random_string(10),
        'password': generate_random_string(10),
        'firstName': generate_random_string(10)
    }


@pytest.fixture
def existing_courier():
    payload = register_new_courier_and_return_login_password()
    return {
        'login': payload[0],
        'password': payload[1],
        'firstName': payload[2]
    }

