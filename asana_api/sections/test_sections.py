"""
(c) Copyright Jalasoft. 2024

test_sections.py
    file that contains pytest tests for sections endpoint
"""
import logging

import allure
import pytest

from config.config import URL_ASANA
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("ASANA API")
@allure.story("Sections")
class TestSections:
    """
    Class to test section endpoint
    """
    @classmethod
    def setup_class(cls):
        """
        Setup Class to initialize variables or objects
        """
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_ASANA}/projects"
        cls.url_sections = f"{URL_ASANA}/sections"
        cls.list_sections = []
        cls.rest_client = RestClient()

    @allure.feature("List Sections")
    @allure.title("Test get all sections")
    @allure.description("Test that show the response of list of all sections")
    @allure.tag("acceptance", "sections")
    @pytest.mark.acceptance
    def test_get_all_sections_project(self, create_project, _test_log_name):
        """
        Test get all sections of a project
        """
        url_get_all_sections = f"{self.url_projects}/{create_project}/sections"
        response = self.rest_client.request("get", url=url_get_all_sections)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Create Section")
    @allure.title("Test create section")
    @allure.description("Test that show the response of create section")
    @allure.tag("acceptance", "sections")
    @pytest.mark.acceptance
    def test_create_section(self, create_project, _test_log_name):
        """
        Test create section
        """
        url_create_sections = f"{self.url_projects}/{create_project}/sections"
        body_section = {
            "name": "Test Section 1"
        }
        response = self.rest_client.request("post", url=url_create_sections, body=body_section)
        id_section_created = response["body"]['data']['gid']
        self.list_sections.append(id_section_created)
        assert response["status_code"] == 201, "wrong status code, expected 201"

    @allure.feature("Delete Section")
    @allure.title("Test delete section")
    @allure.description("Test that show the response of delete a section")
    @allure.tag("acceptance", "sections")
    @pytest.mark.acceptance
    def test_delete_section(self, create_section, _test_log_name):
        """
        Test delete section
        """
        id_delete_section = create_section['data']['gid']
        LOGGER.debug("Section to delete: %s", id_delete_section)
        url_delete_section = f"{self.url_sections}/{id_delete_section}"
        response = self.rest_client.request("delete", url=url_delete_section)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Update Section")
    @allure.title("Test update section")
    @allure.description("Test that show the response of update a section")
    @allure.tag("acceptance", "sections")
    @pytest.mark.acceptance
    def test_update_section(self,create_section, _test_log_name):
        """
        Test update section
        """
        id_update_section = create_section['data']['gid']
        LOGGER.debug("Section to update: %s", id_update_section)
        url_update_section = f"{self.url_sections}/{id_update_section}"
        body_section_update = {
            "name": "Update Section - Edit",
        }
        response = self.rest_client.request("put", url=url_update_section, body=body_section_update)
        self.list_sections.append(id_update_section)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all sections created in test
        """
        LOGGER.info("Cleanup sections...")
        for id_section in cls.list_sections:
            url_delete_section = f"{URL_ASANA}/sections/{id_section}"
            response = cls.rest_client.request("delete", url=url_delete_section)
            if response["status_code"] == 200:
                LOGGER.info("Section id: %s deleted", id_section)
