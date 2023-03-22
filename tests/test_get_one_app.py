from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


def test_get_one_app():
    get_response = client.get_all_apps()
    verify_successful_get_response(get_response, count_off_apps=5)
    id_first_app = get_response.as_dict[0]["id"]

    get_response_one_app = client.get_one_app_by_id(id_first_app)
    verify_successful_get_response_one_app(get_response_one_app, id_first_app)


def test_get_one_app_with_bad_id():
    get_response = client.get_all_apps()
    verify_successful_get_response(get_response, count_off_apps=5)
    id_first_app = get_response.as_dict[0]["id"] + "456"

    get_response_one_app = client.get_one_app_by_id(id_first_app)
    verify_valid_get_response(response=get_response_one_app, loc="app_id",
                              message="value is not a valid uuid")

