"""
(c) Copyright Jalasoft. 2024

test_tasks.py
    file that contains pytest tests for tasks endpoint
"""
import logging

import allure
import pytest

from config.config import URL_ASANA
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)

@allure.epic("ASANA API")
@allure.story("Tasks")
class TestTasks:
    """
    Clas for testing tasks endpoints
    """
    @classmethod
    def setup_class(cls):
        """
        Setup Class to initialize variables or objects
        """
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_ASANA}/projects"
        cls.url_sections = f"{URL_ASANA}/sections"
        cls.url_tasks = f"{URL_ASANA}/tasks"
        cls.list_tasks = []
        cls.rest_client = RestClient()

    @allure.feature("List Tasks")
    @allure.title("Test get all tasks")
    @allure.description("Test that show the response of list of all tasks")
    @allure.tag("acceptance", "tasks")
    @pytest.mark.acceptance
    def test_get_all_tasks_project(self, create_project, _test_log_name):
        """
        Test get all tasks of a project
        """
        url_get_all_tasks = f"{URL_ASANA}/tasks?project={create_project}"
        response = self.rest_client.request("get", url=url_get_all_tasks)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Create Task")
    @allure.title("Test create task")
    @allure.description("Test that show the response of create task")
    @allure.tag("acceptance", "tasks")
    @pytest.mark.acceptance
    def test_create_task(self, create_project, _test_log_name):
        """
        Test create task
        """
        body_task = {
            "projects": [
                f"{create_project}"
            ],
            "name": "test 003"
          }
        response = self.rest_client.request("post", url=self.url_tasks, body=body_task)
        id_task_created = response["body"]['data']['gid']
        self.list_tasks.append(id_task_created)
        assert response["status_code"] == 201, "wrong status code, expected 201"

    @allure.feature("Delete Task")
    @allure.title("Test delete task")
    @allure.description("Test that show the response of delete a task")
    @allure.tag("acceptance", "tasks")
    @pytest.mark.acceptance
    def test_delete_task(self, create_task, _test_log_name):
        """
        Test delete task
        """
        url_delete_task = f"{self.url_tasks}/{create_task}"
        response = self.rest_client.request("delete", url=url_delete_task)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    @allure.feature("Update Task")
    @allure.title("Test update task")
    @allure.description("Test that show the response of update a task")
    @allure.tag("acceptance", "tasks")
    @pytest.mark.acceptance
    def test_update_task(self, create_task, _test_log_name):
        """
        Test update task
        """
        LOGGER.debug("Task to update: %s", create_task)
        url_update_task = f"{self.url_tasks}/{create_task}"
        body_task_update = {
            "name": "Task Updated",
        }
        response = self.rest_client.request("put", url=url_update_task, body=body_task_update)
        self.list_tasks.append(create_task)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        Delete all sections created in test
        """
        LOGGER.info("Cleanup sections...")
        for id_task in cls.list_tasks:
            url_delete_task = f"{URL_ASANA}/tasks/{id_task}"
            response = cls.rest_client.request("delete", url=url_delete_task)
            if response["status_code"] == 200:
                LOGGER.info("Section id: %s deleted", id_task)
