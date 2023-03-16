import random
import requests
from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


def test_delete_last_app(create_data):
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
    assert_that(response_1.status_code).is_equal_to(requests.codes.ok)
    for i in response_1.as_dict:
        if i["name"] == expected_name:
            id_app_to_delete = i["id"]

    response_2 = client.delete_app(id_app_to_delete)
    assert_that(response_2.status_code).is_equal_to(204)

    response_3 = client.get_all_apps(params={'limit': 99})
    assert_that(response_3.status_code).is_equal_to(requests.codes.ok)
    for i in response_3.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, App {i['id']} was not deleted")

    response4 = client.get_one_app_by_id(id_app_to_delete)
    one_app = response4.as_dict
    print(one_app["detail"])
    assert_that(response4.status_code).is_equal_to(404)


def test_delete_app_which_not_exist():
    response = client.delete_app("56464864fdfd")
    assert_that(response.status_code).is_equal_to(422)
    one_app = response.as_dict

    assert_that(len(one_app)).is_equal_to(1)
    print(one_app["detail"])
    for i in one_app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("app_id")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("value is not a valid uuid")
        assert_that(i["type"]).is_instance_of(str)
