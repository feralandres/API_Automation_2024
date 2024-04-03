import logging

import pytest
import requests

from config.config import URL_ASANA, WORKSPACE_ASANA
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_project(request):

    LOGGER.debug("Create project fixture")
    # environment = request.config.getoption("--env")
    # LOGGER.critical("Environment selected: %s", environment)
    body_project = {
        "name": "My Work Tasks 3"
    }
    url_project = URL_ASANA+"/workspaces/"+WORKSPACE_ASANA+"/projects"
    rest_client = RestClient()
    response = rest_client.request("post", url_project, body=body_project)
    LOGGER.debug("Response from create project fixture %s", response["body"])
    project_id = response["body"]['data']['gid']

    yield project_id
    delete_project(project_id, rest_client)


@pytest.fixture()
def create_section(get_project):

    LOGGER.debug("Create section fixture")

    project_id = f"{get_project}"
    url_create_sections = f"{URL_ASANA}/projects/{project_id}/sections"
    body_section = {
        "name": "Test Section 2"
    }
    rest_client = RestClient()
    response = rest_client.request("post", url_create_sections, body=body_section)

    return response["body"]

@pytest.fixture()
def create_task(create_project):
    content_body_task = {
        "projects": [
            f"{create_project}"
        ],
        "name": "test 003"
    }
    url_create_tasks = f"{URL_ASANA}/tasks"
    rest_client = RestClient()
    response = rest_client.request("post", url=url_create_tasks, body=content_body_task)
    id_task_created = response["body"]['data']['gid']

    yield id_task_created

@pytest.fixture()
def get_project():
    rest_client = RestClient()
    response = rest_client.request("get", URL_ASANA+"/projects")
    project_id = response["body"]['data'][0]['gid']
    LOGGER.debug("Project ID: %s", project_id)

    return project_id


@pytest.fixture()
def log_test_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)

def delete_project(project_id, rest_client):
    LOGGER.info("Cleanup project...")
    url_delete_project = f"{URL_ASANA}/projects/{project_id}"
    response = rest_client.request("delete", url=url_delete_project)
    if response["status_code"] == 200:
        LOGGER.info("Project id: %s deleted", project_id)

def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where the tests are executed"
    )
    parser.addoption(
        '--browser', action='store', default='chrome', help="Browser type to execute the UI tests"
    )