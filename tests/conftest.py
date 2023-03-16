import random
import pytest
from tests.data.type_app import TypeApp
from utils.file_reader import read_file


@pytest.fixture
def create_data():
    payload = read_file('create_app.json')

    random_choice = random.choice(list(TypeApp))

    payload["name"] = "Example App"
    payload["type"] = random_choice.value

    yield payload
