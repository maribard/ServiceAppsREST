import random
import pytest
from assertpy import assert_that

from clients.apps.apps_client import AppsClient
from tests.data.type_app import TypeApp
from utils.file_reader import read_file


@pytest.fixture
def create_data():
    payload = read_file('create_app.json')

    random_choice = random.choice(list(TypeApp))

    payload["name"] = "Example App"
    payload["type"] = random_choice.value

    yield payload


@pytest.fixture
def random_number(request):
    return random.randint(request.param[0], request.param[1])


def prepare_data():
    payload = read_file('create_app.json')

    random_choice = random.choice(list(TypeApp))

    payload["name"] = "Example App"
    payload["type"] = random_choice.value

    return payload


@pytest.fixture
def setup(request):
    client = AppsClient()

    created_data = prepare_data()
    created_data['name'] = created_data['name'] + f"{random.randint(request.param[0], request.param[1])}"

    name, post_response = client.create_app(created_data)
    yield client, created_data, post_response

    delete_response = client.delete_app(post_response.as_dict["id"])
    assert_that(delete_response.status_code).is_equal_to(204)
