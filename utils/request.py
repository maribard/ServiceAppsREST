from dataclasses import dataclass

import requests


@dataclass
class Response:
    """
    Class which represents returned object methods like get, post, delete, ...
    """
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    """
    This class represents Requests API
    """
    def get(self, url, params=None):
        """
        Send GET reguest
        :param url: URL for the reguest
        :return: Response object
        """
        response = requests.get(url, params)
        return self.__get_responses(response)

    def post(self, url, body, headers):
        """
        Send POST reguest
        :param url: URL for the reguest
        :param body: Request body
        :param headers: Dictionary of HTTP Headers
        :return: Response object
        """
        response = requests.post(url, json=body, headers=headers)
        return self.__get_responses(response)

    def patch(self, url, body, headers):
        """
        Send PATCH reguest
        :param url: URL for the reguest
        :param body: Request body
        :param headers: Dictionary of HTTP Headers
        :return: Response object
        """
        response = requests.patch(url, json=body, headers=headers)
        return self.__get_responses(response)

    def delete(self, url):
        """
        Send DELETE reguest
        :param url: URL for the reguest
        :return: Response object
        """
        response = requests.delete(url)
        return self.__get_responses(response)

    def __get_responses(self, response):
        """
        Get returned object from request and return Response object
        :param response: Response object
        :return: Response object (status_code, text, as_dict, headers)
        """
        status_code = response.status_code
        text = response.text

        try:
            as_dict = response.json()
        except Exception:
            as_dict = {}

        headers = response.headers

        return Response(
            status_code, text, as_dict, headers
        )
