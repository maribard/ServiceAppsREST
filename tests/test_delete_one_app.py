from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *
from tests.conftest import *

client = AppsClient()


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
def test_delete_last_app(create_data, random_number):
    create_data['name'] = create_data['name'] + f"{random_number}"

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_successful_get_response(get_response, count_off_apps=99)
    id_app_to_delete = get_id_app(get_response, name)

    delete_response = client.delete_app(id_app_to_delete)
    assert_that(delete_response.status_code).is_equal_to(204)

    get_response_2 = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response_2, name_app=name)

    get_response_one_app = client.get_one_app_by_id(id_app_to_delete)
    verify_that_app_was_not_found(get_response_one_app)


@pytest.mark.parametrize("id_app_to_delete", ["56464864fdfd"])
def test_delete_app_which_not_exist(id_app_to_delete):
    delete_response = client.delete_app(id_app_to_delete)
    verify_valid_delete_response(response=delete_response, loc="app_id",
                                 message="value is not a valid uuid")

