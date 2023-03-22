from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *
from tests.conftest import *

client = AppsClient()

@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
def test_patch_created_app(create_data, random_number):
    create_data['name'] = create_data['name'] + f"{random_number}"

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_successful_get_response(get_response, count_off_apps=99)
    id_app_to_update = get_id_app(get_response, name)

    list_types = list(TypeApp)
    for i in list_types:
        if i.value == create_data['type']:
            list_types.remove(i)
    random_choice = random.choice(list_types)

    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['type'] = random_choice.value
    create_data['urls'][0] = "http://example.com/787878"

    name, patch_response = client.update_app_by_patch(id_app_to_update, create_data)
    verify_successful_patch_response(patch_response, create_data)

    delete_response = client.delete_app(id_app_to_update)
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
def test_patch_with_bad_id(create_data, random_number):
    create_data['name'] = create_data['name'] + f"{random_number}"

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_successful_get_response(get_response, count_off_apps=99)
    id_app_to_delete = get_id_app(get_response, name)
    id_app_to_update = id_app_to_delete + "5876985"

    list_types = list(TypeApp)
    for i in list_types:
        if i.value == create_data['type']:
            list_types.remove(i)
    random_choice = random.choice(list_types)
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['type'] = random_choice.value
    create_data['urls'][0] = "http://example.com/787878"

    name, patch_response = client.update_app_by_patch(id_app_to_update, create_data)
    verify_valid_patch_response(response=patch_response, loc="app_id",
                                message="value is not a valid uuid")

    delete_response = client.delete_app(id_app_to_delete)
    assert_that(delete_response.status_code).is_equal_to(204)
