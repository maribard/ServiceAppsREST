from clients.apps.base_client import BaseClient
from config import BASE_URI
from utils.request import APIRequest


class AppsClient(BaseClient):
    """
    This class represets API client for ServiceApps
    """
    def __init__(self):
        super().__init__()

        self.base_url = BASE_URI
        self.request = APIRequest()

    def create_app(self, body=None):
        """
        Create app
        :param body: Request body
        :return: Name created APP and Response Object
        """
        name, response = self.__create_app_with_unique_last_name(body)
        return name, response

    def __create_app_with_unique_last_name(self, body):
        name = body["name"]
        response = self.request.post(self.base_url, body, self.headers)
        return name, response

    def get_one_app_by_id(self, app_id):
        """
        Sends a GET request
        :param app_id:
        :return: Response Object
        """
        new_url = self.base_url + f"{app_id}"
        print(new_url)
        return self.request.get(new_url)

    def get_all_apps(self, params=None):
        """
        Sends a GET request
        :return: Response Object
        """
        return self.request.get(self.base_url, params)

    def update_app_by_patch(self, app_id, body):
        """
        Sends a PATCH request

        :param body:
        :return: Updated name APP and Response Object
        """
        name = body["name"]
        url = f'{self.base_url}/{app_id}'
        response = self.request.patch(url, body, self.headers)
        return name, response

    def delete_app(self, app_id):
        """
        Sends a DELETE request

        :param body:
        :return: Response Object
        """
        url = f'{self.base_url}/{app_id}'
        return self.request.delete(url)
