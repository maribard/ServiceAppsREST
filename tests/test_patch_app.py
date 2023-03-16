import requests
import random
from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *
from tests.data.type_app import TypeApp

client = AppsClient()


def test_patch_created_app(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    app = response.as_dict

    expected_name = created_data['name']
    expected_type = created_data['type']
    expected_urls = created_data['urls']

    assert_that(app["name"]).is_instance_of(str)
    assert_that(len(app["name"])).is_between(0, 60)
    assert_that(app["name"]).is_equal_to(expected_name)

    assert_that(app["type"]).is_instance_of(str)
    assert_that(app["type"]).is_equal_to(expected_type)

    assert_that(len(app["urls"])).is_between(1, 2083)
    assert_that(app["urls"]).is_equal_to(expected_urls)

    assert_that(app["id"]).is_instance_of(str)
    assert_that(app["created_at"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})
    for i in response_1.as_dict:
        if i["name"] == expected_name:
            id_app_to_update = i["id"]

    list_types = list(TypeApp)
    for i in list_types:
        if i.value == created_data['type']:
            list_types.remove(i)
    random_choice = random.choice(list_types)
    created_data['name'] = created_data['name'] + f"{random_no}"
    created_data['type'] = random_choice.value
    created_data['urls'][0] = "http://example.com/787878"

    expected_name2 = created_data['name']
    expected_type2 = created_data['type']
    expected_urls2 = created_data['urls']

    name, response_2 = client.update_app_by_patch(id_app_to_update, created_data)
    assert_that(response_2.status_code).is_equal_to(200)

    one_app = response_2.as_dict

    assert_that(one_app["name"]).is_instance_of(str)
    assert_that(len(one_app["name"])).is_between(0, 60)
    assert_that(one_app["name"]).is_equal_to(expected_name2)

    assert_that(one_app["type"]).is_instance_of(str)
    assert_that(one_app["type"]).is_equal_to(expected_type2)

    assert_that(len(one_app["urls"])).is_between(1, 2083)
    assert_that(one_app["urls"]).is_equal_to(expected_urls2)

    assert_that(one_app["id"]).is_instance_of(str)
    assert_that(one_app["id"]).is_equal_to(id_app_to_update)
    assert_that(one_app["created_at"]).is_instance_of(str)

    response_3 = client.delete_app(id_app_to_update)
    assert_that(response_3.status_code).is_equal_to(204)


def test_patch_with_bad_id(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    app = response.as_dict

    expected_name = created_data['name']
    expected_type = created_data['type']
    expected_urls = created_data['urls']

    assert_that(app["name"]).is_instance_of(str)
    assert_that(len(app["name"])).is_between(0, 60)
    assert_that(app["name"]).is_equal_to(expected_name)

    assert_that(app["type"]).is_instance_of(str)
    assert_that(app["type"]).is_equal_to(expected_type)

    assert_that(len(app["urls"])).is_between(1, 2083)
    assert_that(app["urls"]).is_equal_to(expected_urls)

    assert_that(app["id"]).is_instance_of(str)
    assert_that(app["created_at"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})
    for i in response_1.as_dict:
        if i["name"] == expected_name:
            id_app_to_update = i["id"] + "5876985"
            id_app_to_delete = i["id"]

    list_types = list(TypeApp)
    for i in list_types:
        if i.value == created_data['type']:
            list_types.remove(i)
    random_choice = random.choice(list_types)
    created_data['name'] = created_data['name'] + f"{random_no}"
    created_data['type'] = random_choice.value
    created_data['urls'][0] = "http://example.com/787878"

    name, response_2 = client.update_app_by_patch(id_app_to_update, created_data)
    assert_that(response_2.status_code).is_equal_to(422)
    app = response_2.as_dict

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("app_id")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("value is not a valid uuid")
        assert_that(i["type"]).is_instance_of(str)

    response_3 = client.delete_app(id_app_to_delete)
    assert_that(response_3.status_code).is_equal_to(204)
