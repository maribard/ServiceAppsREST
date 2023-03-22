from tests.conftest import *
from clients.apps.apps_client import AppsClient
from tests.assertions.apps_assertions import *

client = AppsClient()


@pytest.mark.parametrize("limit", [5])
def test_get_all_apps_with_default_param(limit):
    response = client.get_all_apps()
    verify_successful_get_response(response, count_off_apps=limit)


@pytest.mark.parametrize("offset,limit", [(1, 5)])
def test_get_all_apps_with_min_normal_offset(offset, limit):
    response_1 = client.get_all_apps()
    response_2 = client.get_all_apps(params={'offset': offset})

    verify_successful_get_response(response_1, count_off_apps=limit)
    verify_successful_get_response(response_2, count_off_apps=limit)

    assert_that(response_1.as_dict[1]["name"]).is_equal_to(response_2.as_dict[0]["name"])
    assert_that(response_1.as_dict[1]["type"]).is_equal_to(response_2.as_dict[0]["type"])
    assert_that(response_1.as_dict[1]["urls"]).is_equal_to(response_2.as_dict[0]["urls"])
    assert_that(response_1.as_dict[1]["id"]).is_equal_to(response_2.as_dict[0]["id"])
    assert_that(response_1.as_dict[1]["created_at"]).is_equal_to(response_2.as_dict[0]["created_at"])


@pytest.mark.parametrize("offset,limit", [(99, 99)])
def test_get_all_apps_with_max_normal_offset(offset, limit):
    response_1 = client.get_all_apps(params={'offset': offset})
    assert_that(len(response_1.as_dict)).is_equal_to(0)

    response_2 = client.get_all_apps(params={'limit': limit})
    count_of_apps = len(response_2.as_dict)
    print(f"Amount of returned apps: {count_of_apps}")

    response_3 = client.get_all_apps(params={'offset': count_of_apps})
    assert_that(len(response_3.as_dict)).is_equal_to(0)

    response_4 = client.get_all_apps(params={'offset': count_of_apps - 1})
    verify_successful_get_response(response_4, count_off_apps=1)


@pytest.mark.parametrize("offset", [0])
def test_get_all_apps_with_min_abnormal_offset(offset):
    response = client.get_all_apps(params={'offset': offset})
    verify_valid_get_response(response=response, loc="offset",
                              message="ensure this value is greater than 0")


@pytest.mark.parametrize("offset", [100])
def test_get_all_apps_with_max_abnormal_offset(offset):
    response = client.get_all_apps(params={'offset': offset})
    verify_valid_get_response(response=response, loc="offset",
                              message="ensure this value is less than 100")


@pytest.mark.parametrize("limit", [1])
def test_get_all_apps_with_min_normal_limit(limit):
    response = client.get_all_apps(params={'limit': limit})
    verify_successful_get_response(response, count_off_apps=limit)


@pytest.mark.parametrize("limit", [99])
def test_get_all_apps_with_max_normal_limit(limit):
    response = client.get_all_apps(params={'limit': limit})
    verify_successful_get_response(response, count_off_apps=limit)


@pytest.mark.parametrize("limit", [0])
def test_get_all_apps_with_min_abnormal_limit(limit):
    response = client.get_all_apps(params={'limit': limit})
    verify_valid_get_response(response=response, loc="limit",
                              message="ensure this value is greater than 0")


@pytest.mark.parametrize("limit", [100])
def test_get_all_apps_with_max_abnormal_limit(limit):
    response = client.get_all_apps(params={'limit': limit})
    verify_valid_get_response(response=response, loc="limit",
                              message="ensure this value is less than 100")
