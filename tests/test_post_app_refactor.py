from tests.assertions.apps_assertions import *
from tests.conftest import *


@pytest.mark.parametrize("setup", [(0, 1000)], indirect=True)
def test_app_can_be_added_with_a_json_template(setup):
    client, create_data, post_response = setup
    verify_successful_post_response(post_response, create_data)

    get_response = client.get_all_apps(params={'limit': 99})
    verify_if_app_exist_in_get_response(get_response, name_app=create_data['name'])
