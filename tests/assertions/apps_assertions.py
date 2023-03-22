from assertpy import assert_that

import requests


def verify_successful_get_response(response, count_off_apps=5):
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    assert_that(len(response.as_dict)).is_less_than_or_equal_to(count_off_apps)

    for i in response.as_dict:
        assert_that(i["name"]).is_instance_of(str)
        assert_that(len(i["name"])).is_between(0, 60)

        assert_that(i["type"]).is_instance_of(str)
        assert_that(i["type"]).is_in("sharepoint", "web", "mobile")

        assert_that(len(i["urls"])).is_between(1, 2083)

        assert_that(i["id"]).is_instance_of(str)
        assert_that(i["created_at"]).is_instance_of(str)


def verify_successful_get_response_one_app(response, id_app):
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    one_app = response.as_dict

    assert_that(one_app["name"]).is_instance_of(str)
    assert_that(len(one_app["name"])).is_between(0, 60)

    assert_that(one_app["type"]).is_instance_of(str)
    assert_that(one_app["type"]).is_in("sharepoint", "web", "mobile")

    assert_that(len(one_app["urls"])).is_between(1, 2083)

    assert_that(one_app["id"]).is_instance_of(str)
    assert_that(one_app["created_at"]).is_instance_of(str)

    assert_that(one_app["id"]).is_equal_to(id_app)


def verify_valid_get_response(response, loc, message):
    assert_that(response.status_code).is_equal_to(422)
    assert_that(len(response.as_dict)).is_equal_to(1)

    for i in response.as_dict["detail"]:
        print(i["loc"])
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to(loc)

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to(message)
        assert_that(i["type"]).is_instance_of(str)


def verify_successful_post_response(response, create_data):
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_as_dict = response.as_dict

    assert_that(response_as_dict["name"]).is_instance_of(str)
    assert_that(len(response_as_dict["name"])).is_between(0, 60)
    assert_that(response_as_dict["name"]).is_equal_to(create_data['name'])

    assert_that(response_as_dict["type"]).is_instance_of(str)
    assert_that(response_as_dict["type"]).is_equal_to(create_data['type'])

    assert_that(len(response_as_dict["urls"])).is_between(1, 2083)
    assert_that(response_as_dict["urls"]).is_equal_to(create_data['urls'])

    assert_that(response_as_dict["id"]).is_instance_of(str)
    assert_that(response_as_dict["created_at"]).is_instance_of(str)


def verify_if_app_exist_in_get_response(response, name_app):
    for i in response.as_dict:
        if i["name"] == name_app:
            return

    raise Exception(f"Sorry, there is no app with name {name_app} in GET response")


def verify_valid_post_response(response, loc, message):
    assert_that(response.status_code).is_equal_to(422)
    assert_that(len(response.as_dict)).is_equal_to(1)

    for i in response.as_dict["detail"]:
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][2]).is_equal_to(loc)

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to(message)
        assert_that(i["type"]).is_instance_of(str)


def verify_if_app_not_exist_in_get_response(response, name_app):
    for i in response.as_dict:
        if i["name"] == name_app:
            raise Exception(f"Sorry, app with name {name_app} exist")


def verify_valid_delete_response(response, loc, message):
    assert_that(response.status_code).is_equal_to(422)
    assert_that(len(response.as_dict)).is_equal_to(1)

    for i in response.as_dict["detail"]:
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to(loc)

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to(message)
        assert_that(i["type"]).is_instance_of(str)


def get_id_app(response, app_name):
    for i in response.as_dict:
        if i["name"] == app_name:
            return i["id"]


def verify_that_app_was_not_found(response):
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.as_dict["detail"]).is_equal_to("App with given id not found")


def verify_successful_patch_response(response, create_data):
    assert_that(response.status_code).is_equal_to(requests.codes.ok)
    response_as_dict = response.as_dict

    assert_that(response_as_dict["name"]).is_instance_of(str)
    assert_that(len(response_as_dict["name"])).is_between(0, 60)
    assert_that(response_as_dict["name"]).is_equal_to(create_data['name'])

    assert_that(response_as_dict["type"]).is_instance_of(str)
    assert_that(response_as_dict["type"]).is_equal_to(create_data['type'])

    assert_that(len(response_as_dict["urls"])).is_between(1, 2083)
    assert_that(response_as_dict["urls"]).is_equal_to(create_data['urls'])

    assert_that(response_as_dict["id"]).is_instance_of(str)
    assert_that(response_as_dict["created_at"]).is_instance_of(str)


def verify_valid_patch_response(response, loc, message):
    assert_that(response.status_code).is_equal_to(422)
    assert_that(len(response.as_dict)).is_equal_to(1)

    for i in response.as_dict["detail"]:
        assert_that(i["loc"]).is_instance_of(list)
        assert_that(i["loc"][1]).is_equal_to(loc)

        assert_that(i["msg"]).is_instance_of(str)
        assert_that(i["msg"]).is_equal_to(message)
        assert_that(i["type"]).is_instance_of(str)