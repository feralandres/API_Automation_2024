import logging


from config.config import URL_ASANA, WORKSPACE_ASANA
from helpers.rest_client import RestClient
from utils.logger import get_logger


LOGGER = get_logger(__name__, logging.DEBUG)


class TestProjects:

    @classmethod
    def setup_class(cls):
        LOGGER.debug("SetupClass method")
        cls.url_projects = f"{URL_ASANA}/projects"
        cls.url_workspaces = f"{URL_ASANA}/workspaces/{WORKSPACE_ASANA}/projects"
        cls.list_projects = []
        cls.rest_client = RestClient()

    def test_get_all_projects(self, log_test_name):

        response = self.rest_client.request("get", url=self.url_projects)

        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_create_project_in_workspace(self, log_test_name):

        body_project = {
            "name": "My Work Tasks",
        }
        response = self.rest_client.request("post", url=self.url_workspaces, body=body_project)

        id_project_created = response["body"]['data']['gid']
        self.list_projects.append(id_project_created)
        assert response["status_code"] == 201, "wrong status code, expected 201"

    def test_delete_project(self, create_project, log_test_name):
        # id_project_delete = create_project['data']['gid']
        url_asana_delete = f"{self.url_projects}/{create_project}"

        response = self.rest_client.request("delete", url=url_asana_delete)
        assert response["status_code"] == 200, "wrong status code, expected 200"

    def test_update_project(self, create_project, log_test_name):
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
