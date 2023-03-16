import requests
import random
from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


def test_app_can_be_added_with_a_json_template(create_data):
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
            return

    raise Exception("Sorry, there is no created app in GET request")


def test_app_cannot_be_added_with_a_json_template(create_data):
    created_data = create_data
    random_no = random.randint(1000, 9999)
    string = "sssssssssssssssssssssssssss"
    created_data['name'] = f"Example App with 61 characters{random_no}" + string

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("name")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value has at most 60 characters")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")


def test_app_can_be_added_with_a_json_template_max_char_name(create_data):
    created_data = create_data
    random_no = random.randint(1000, 9999)
    string = "ssssssssssssssssssssssssss"
    created_data["name"] = f"Example App with 60 characters{random_no}" + string

    name, response = client.create_app(create_data)
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
            return

    raise Exception("Sorry, there is no created app in GET request")


def test_app_can_be_added_with_a_json_template_min_char_name(create_data):
    created_data = create_data
    created_data["name"] = f""

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
            return

    raise Exception("Sorry, there is no created app in GET request")


def test_app_cannot_be_added_with_a_json_template_with_bad_type(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    created_data['type'] = "something"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("type")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("value is not a valid enumeration member; permitted: 'web', 'mobile', 'sharepoint'")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")


def test_app_cannot_be_added_with_a_json_template_with_small_urls(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    created_data['urls'][0] = ""

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("urls")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value has at least 1 characters")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")


def test_app_cannot_be_added_with_a_json_template_with_bad_value_url(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    created_data['urls'][0] = "g"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("urls")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("invalid or missing URL scheme")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")


def test_app_cannot_be_added_with_a_json_template_url_host_invalid(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    host = "x" * 2000
    created_data['urls'][0] = "https://" + f"{host}" + ".com"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("urls")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("URL host invalid")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")


def test_app_can_be_added_with_a_json_template_min_char_name(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    path = "x" * 2063
    created_data['urls'][1] = created_data['urls'][0] + f"/{path}"

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
            return

    raise Exception("Sorry, there is no created app in GET request")


def test_app_cannot_be_added_with_a_json_template_url_len_invalid(create_data):
    created_data = create_data
    random_no = random.randint(0, 1000)
    created_data['name'] = created_data['name'] + f"{random_no}"
    path = "x" * 2064
    created_data['urls'][1] = created_data['urls'][0] + f"/{path}"

    name, response = client.create_app(created_data)
    assert_that(response.status_code).is_equal_to(422)
    app = response.as_dict
    expected_name = created_data['name']

    assert_that(len(app)).is_equal_to(1)
    print(app["detail"])
    for i in app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to("urls")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value has at most 2083 characters")
        assert_that(i["type"]).is_instance_of(str)

    response_1 = client.get_all_apps(params={'limit': 99})

    for i in response_1.as_dict:
        if i["name"] == expected_name:
            raise Exception(f"Sorry, app with name {expected_name} was created")