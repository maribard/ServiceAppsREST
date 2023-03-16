import requests

from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


def test_get_all_apps_with_default_param():
    response = client.get_all_apps()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(len(response.as_dict)).is_equal_to(5)
    for i in response.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)


def test_get_all_apps_with_min_normal_offset():
    response_1 = client.get_all_apps()
    response_2 = client.get_all_apps(params={'offset': 1})
    assert_that(response_1.status_code).is_equal_to(requests.codes.ok)
    assert_that(response_2.status_code).is_equal_to(requests.codes.ok)

    assert_that(len(response_1.as_dict)).is_equal_to(5)
    assert_that(len(response_2.as_dict)).is_equal_to(5)


    for i in response_1.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)

    for i in response_2.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)

    assert_that(response_1.as_dict[1]["name"]).is_equal_to(response_2.as_dict[0]["name"])
    assert_that(response_1.as_dict[1]["type"]).is_equal_to(response_2.as_dict[0]["type"])
    assert_that(response_1.as_dict[1]["urls"]).is_equal_to(response_2.as_dict[0]["urls"])
    assert_that(response_1.as_dict[1]["id"]).is_equal_to(response_2.as_dict[0]["id"])
    assert_that(response_1.as_dict[1]["created_at"]).is_equal_to(response_2.as_dict[0]["created_at"])

def test_get_all_apps_with_max_normal_offset():
    response_1 = client.get_all_apps(params={'limit': 99})
    count_of_apps = len(response_1.as_dict)
    print(count_of_apps)

    response_2 = client.get_all_apps(params={'offset': count_of_apps})
    assert_that(len(response_2.as_dict)).is_equal_to(0)

    response_3 = client.get_all_apps(params={'offset': count_of_apps-1})
    assert_that(len(response_3.as_dict)).is_equal_to(1)

    response_4 = client.get_all_apps(params={'offset': 99})
    assert_that(len(response_4.as_dict)).is_equal_to(0)

def test_get_all_apps_with_min_abnormal_offset():
    response = client.get_all_apps(params={'offset': 0})
    assert_that(response.status_code).is_equal_to(422)

    assert_that(len(response.as_dict)).is_equal_to(1)
    print(response.as_dict["detail"])
    for i in response.as_dict["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("offset")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value is greater than 0")
        assert_that(i["type"]).is_instance_of(str)


def test_get_all_apps_with_max_abnormal_offset():
    response = client.get_all_apps(params={'offset': 100})
    assert_that(response.status_code).is_equal_to(422)

    assert_that(len(response.as_dict)).is_equal_to(1)
    print(response.as_dict["detail"])
    for i in response.as_dict["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("offset")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value is less than 100")
        assert_that(i["type"]).is_instance_of(str)


def test_get_all_apps_with_min_normal_limit():
    response = client.get_all_apps(params={'limit': 1})
    assert_that(response.status_code).is_equal_to(200)

    assert_that(len(response.as_dict)).is_equal_to(1)
    for i in response.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)


def test_get_all_apps_with_max_normal_limit():
    response = client.get_all_apps(params={'limit': 99})
    assert_that(response.status_code).is_equal_to(200)

    assert_that(len(response.as_dict)).is_less_than(100)
    for i in response.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)


def test_get_all_apps_with_min_abnormal_limit():
    response = client.get_all_apps(params={'limit': 0})
    assert_that(response.status_code).is_equal_to(422)

    assert_that(len(response.as_dict)).is_equal_to(1)
    print(response.as_dict["detail"])
    for i in response.as_dict["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("limit")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value is greater than 0")
        assert_that(i["type"]).is_instance_of(str)


def test_get_all_apps_with_max_abnormal_limit():
    response = client.get_all_apps(params={'limit': 100})
    assert_that(response.status_code).is_equal_to(422)

    assert_that(len(response.as_dict)).is_equal_to(1)
    print(response.as_dict["detail"])
    for i in response.as_dict["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("limit")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("ensure this value is less than 100")
        assert_that(i["type"]).is_instance_of(str)







