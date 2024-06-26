import json
import logging

import requests

from config.config import HEADERS_ASANA
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:

    def __init__(self, headers=HEADERS_ASANA):
        self.session = requests.Session()

        self.session.headers.update(headers)

    def request(self, method_name, url, body=None):
        """
        Method to call to request methods
        :param method_name:     GET, POST, PUT, DELETE
        :param url:
        :param body:            body to use in request
        :return:
        """
        response_dict = {}
        try:
            response = self.select_method(method_name, self.session)(url=url, data=body)
            LOGGER.debug("Status Code %s", response.status_code)
            LOGGER.debug("Response Content %s", response.text)
            response.raise_for_status()
            if hasattr(response, "request"):
                LOGGER.info("Response headers: %s", response.headers)
                response_dict["body"] = json.loads(response.text)

        except requests.exceptions.HTTPError as http_error:
            LOGGER.error("HTTP error: %s", http_error)

        except requests.exceptions.RequestException as request_error:
            LOGGER.error("Request error: %s", request_error)
        finally:
            if response.text:
                response_dict["body"] = json.loads(response.text)
            else:
                response_dict["body"] = {"msg": "No body content"}
            response_dict["status_code"] = response.status_code

        return response_dict

    @staticmethod
    def select_method(method_name, session):
        methods = {
            "get": session.get,
            "post": session.post,
            "delete": session.delete,
            "put": session.put
        }
        return methods.get(method_name)
