from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *
from tests.conftest import *

client = AppsClient()


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
def test_app_can_be_added_with_a_json_template(create_data, random_number):
    create_data['name'] = create_data['name'] + f"{random_number}"

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_exist_in_get_response(get_response, name_app=create_data['name'])

    delete_response = client.delete_app(post_response.as_dict["id"])
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.parametrize("app_name", [""])
def test_app_can_be_added_with_a_json_template_min_char_name(create_data, app_name):
    create_data["name"] = app_name

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_exist_in_get_response(get_response, name_app=create_data['name'])

    delete_response = client.delete_app(post_response.as_dict["id"])
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.parametrize("random_number", [(1000, 9999)], indirect=True)
@pytest.mark.parametrize("norm_len_of_string", ["ssssssssssssssssssssssssss"])
def test_app_can_be_added_with_a_json_template_max_char_name(create_data, random_number, norm_len_of_string):
    create_data["name"] = f"Example App with 60 characters{random_number}" + norm_len_of_string

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response.as_dict, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_exist_in_get_response(get_response, name_app=create_data['name'])

    delete_response = client.delete_app(post_response.as_dict["id"])
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.parametrize("random_number", [(1000, 9999)], indirect=True)
@pytest.mark.parametrize("abn_len_of_string", ["sssssssssssssssssssssssssss"])
def test_app_cannot_be_added_with_a_json_template_abn_max_char_name(create_data, random_number, abn_len_of_string):
    create_data['name'] = f"Example App with 61 characters{random_number}" + abn_len_of_string

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="name",
                               message="ensure this value has at most 60 characters")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("app_type", ["something"])
def test_app_cannot_be_added_with_a_json_template_with_bad_type(create_data, random_number, app_type):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['type'] = app_type

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="type",
                               message="value is not a valid enumeration member; permitted:"
                                       " 'web', 'mobile', 'sharepoint'")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 9999)], indirect=True)
@pytest.mark.parametrize("path", ["x" * 2063])
def test_app_can_be_added_with_a_json_template_max_char_url(create_data, random_number, path):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][1] = create_data['urls'][0] + f"/{path}"

    name, post_response = client.create_app(create_data)
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_exist_in_get_response(get_response, name_app=create_data['name'])

    delete_response = client.delete_app(post_response.as_dict["id"])
    assert_that(delete_response.status_code).is_equal_to(204)


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("app_url", [""])
def test_app_cannot_be_added_with_a_json_template_with_small_urls(create_data, random_number, app_url):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = app_url

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="ensure this value has at least 1 characters")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("app_url", ["g"])
def test_app_cannot_be_added_with_a_json_template_with_bad_value_url(create_data, random_number, app_url):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = app_url

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="invalid or missing URL scheme")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("host", ["x" * 2000])
def test_app_cannot_be_added_with_a_json_template_url_host_invalid(create_data, random_number, host):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = "https://" + f"{host}" + ".com"

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="URL host invalid")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("host", [""])
def test_app_cannot_be_added_with_a_json_template_url_host_missing(create_data, random_number, host):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = "https://" + f"{host}" + ".com"

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="URL host invalid")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("path", ["x" * 2064])
def test_app_cannot_be_added_with_a_json_template_url_len_invalid(create_data, random_number, path):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][1] = create_data['urls'][0] + f"/{path}"

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="ensure this value has at most 2083 characters")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("host", ["s"])
def test_app_cannot_be_added_with_a_json_template_url_host_top_level_invalid(create_data, random_number, host):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = "https://" + f"{host}"

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="URL host invalid, top level domain required")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])


@pytest.mark.parametrize("random_number", [(0, 1000)], indirect=True)
@pytest.mark.parametrize("url", ["htt://f.pl"])
def test_app_cannot_be_added_with_a_json_template_url_scheme_not_permitted(create_data, random_number, url):
    create_data['name'] = create_data['name'] + f"{random_number}"
    create_data['urls'][0] = url

    name, post_response = client.create_app(create_data)
    verify_valid_post_response(response=post_response, loc="urls",
                               message="URL scheme not permitted")

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_not_exist_in_get_response(get_response, name_app=create_data['name'])
