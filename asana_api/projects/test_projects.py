"""
(c) Copyright Jalasoft. 2024

test_projects.py
    file that contains pytest tests for projects endpoint
"""
import logging

import allure
import pytest

from config.config import URL_ASANA, WORKSPACE_ASANA
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


@allure.epic("ASANA API")
@allure.story("Projects")
class TestProjects:
    """
    Class for Test projects endpoint
    """
    @classmethod
    def setup_class(cls):
        """
        Setup Class to initialize variables or objects
        """
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_ASANA}/projects"
        cls.url_workspaces = f"{URL_ASANA}/workspaces/{WORKSPACE_ASANA}/projects"
        cls.list_projects = []
        cls.rest_client = RestClient()

    @allure.feature("List Projects")
    @allure.title("Test get all projects")
    @allure.description("Test that show the response of list of all projects")
    @allure.tag("acceptance", "projects")
    @pytest.mark.acceptance
    def test_get_all_projects(self, _test_log_name):
        """
        Test get all projects
        """
        response = self.rest_client.request("get", url=self.url_projects)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Create Project")
    @allure.title("Test create project in a workspace")
    @allure.description("Test that show the response of create project")
    @allure.tag("acceptance", "projects")
    @pytest.mark.acceptance
    def test_create_project_in_workspace(self, _test_log_name):
        """
        Test create project
        """
        body_project = {
            "name": "My Work Tasks",
        }
        response = self.rest_client.request("post", url=self.url_workspaces, body=body_project)

        id_project_created = response["body"]['data']['gid']
        self.list_projects.append(id_project_created)
        assert response["status_code"] == 201, "wrong status code, expected 201"

    @allure.feature("Create Project")
    @allure.title("Test create project in a invalid workspace")
    @allure.description("Test that show the response of create project in a invalid workspace")
    @allure.tag("functional", "projects")
    @pytest.mark.functional
    def test_create_project_invalid_workspace(self, _test_log_name):
        """
        Test create project with invalid workspace
        """
        url_invalid_workspace = f"{URL_ASANA}/workspaces/1234567890/projects"
        body_project = {
            "name": "My Work Tasks",
        }
        response = self.rest_client.request("post", url=url_invalid_workspace, body=body_project)
        assert response["status_code"] == 404, "wrong status code, expected 404"

    @allure.feature("Delete Project")
    @allure.title("Test delete project")
    @allure.description("Test that show the response of delete a project")
    @allure.tag("acceptance", "projects")
    @pytest.mark.acceptance
    def test_delete_project(self, create_project, _test_log_name):
        """
        Test delete project
        """
        # id_project_delete = create_project['data']['gid']
        url_asana_delete = f"{self.url_projects}/{create_project}"

        response = self.rest_client.request("delete", url=url_asana_delete)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Delete Project")
    @allure.title("Test delete invalid project")
    @allure.description("Test that show the response of delete a invalid project")
    @allure.tag("functional", "projects")
    @pytest.mark.functional
    def test_delete_invalid_project(self, _test_log_name):
        """
        Test delete a invalid project
        """
        url_asana_delete_invalid = f"{self.url_projects}/{123456789}"

        response = self.rest_client.request("delete", url=url_asana_delete_invalid)
        assert response["status_code"] == 404, "wrong status code, expected 404"

    @allure.feature("Update Project")
    @allure.title("Test update project")
    @allure.description("Test that show the response of update a project")
    @allure.tag("acceptance", "projects")
    @pytest.mark.acceptance
    def test_update_project(self, create_project, _test_log_name):
        """
        Test update project
        """
        url_asana_update = f"{self.url_projects}/{create_project}"
        LOGGER.debug("Project to update: %s", create_project)
        body_project = {
            "name": "Project Update",
        }
        response = self.rest_client.request("put", url=url_asana_update, body=body_project)
        # Add to list off projects to be deleted in cleanup
        self.list_projects.append(create_project)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all projects created in test
        """
        LOGGER.info("Cleanup projects...")
        for id_project in cls.list_projects:
            url_delete_project = f"{URL_ASANA}/projects/{id_project}"
            response = cls.rest_client.request("delete", url=url_delete_project)
            if response["status_code"] == 200:
                LOGGER.info("Project id: %s deleted", id_project)
