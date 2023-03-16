from assertpy import assert_that


def assert_app_is_present(is_new_app_created):
    assert_that(is_new_app_created).is_not_empty()