import requests
from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


def test_get_one_app():
    response = client.get_all_apps()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(len(response.as_dict)).is_equal_to(5)
    apps = response.as_dict

    id_first_app = apps[0]["id"]
    response1 = client.get_one_app_by_id(id_first_app)
    assert_that(response1.status_code).is_equal_to(requests.codes.ok)
    one_app = response1.as_dict

    assert_that(one_app["name"]).is_instance_of(str)
    assert_that(len(one_app["name"])).is_between(0, 60)

    assert_that(one_app["type"]).is_instance_of(str)
    assert_that(one_app["type"]).is_in("sharepoint", "web", "mobile")

    assert_that(len(one_app["urls"])).is_between(1, 2083)

    assert_that(one_app["id"]).is_instance_of(str)
    assert_that(one_app["created_at"]).is_instance_of(str)

    assert_that(one_app["id"]).is_equal_to(id_first_app)


def test_get_one_app_with_bad_id():
    response = client.get_all_apps()
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(len(response.as_dict)).is_equal_to(5)
    apps = response.as_dict

    id_first_app = apps[0]["id"] + "456"
    response1 = client.get_one_app_by_id(id_first_app)
    assert_that(response1.status_code).is_equal_to(422)
    one_app = response1.as_dict

    assert_that(len(one_app)).is_equal_to(1)
    print(one_app["detail"])
    for i in one_app["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to("app_id")

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to("value is not a valid uuid")
        assert_that(i["type"]).is_instance_of(str)
