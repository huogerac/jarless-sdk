import os

from .api import api_send_output_values


class ApiClient(object):
    @classmethod
    def api(cls):
        return cls()

    def __init__(self):
        self.response = None

    def send_output_values(self, values, **kwargs):
        """
        Send a values (dict) to the task execution output
        """
        package_name = kwargs.get("package_name", os.getenv("PACKAGE"))
        task_id = kwargs.get("task_id", os.getenv("TASK_ID"))
        secrets = kwargs.get("secrets", os.getenv("SECRETS"))

        if not package_name:
            raise RuntimeError("A package_name is required")
        if not task_id:
            raise RuntimeError("A task_id is required")
        if not secrets:
            raise RuntimeError("A secrets is required")

        self.response = api_send_output_values(package_name, task_id, values, secrets)
