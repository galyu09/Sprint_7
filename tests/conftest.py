import pytest

from tests.test_create_courier import register_new_courier_and_return_login_password, \
    generate_random_string_for_test_data


@pytest.fixture
def courier():
    return {
        'login': generate_random_string_for_test_data(10),
        'password': generate_random_string_for_test_data(10),
        'firstName': generate_random_string_for_test_data(10)
    }


@pytest.fixture
def existing_courier():
    login, password, firstName = register_new_courier_and_return_login_password()
    return {
        'login': login,
        'password': password,
        'firstName': firstName
    }