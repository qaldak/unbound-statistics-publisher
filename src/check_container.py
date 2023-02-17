from python_on_whales import docker


class Container:
    def __init__(self, name):
        self.name = name

    # Todo: Debug Logger
    # def __get_container_info(self):
    #     container_info = docker.ps(filters={"name": self.name, "status": "running"})
    #     for container in container_info:
    #         print(container.state)

    def is_running(self):
        if docker.ps(filters={"name": self.name, "status": "running"}):
            return True
        else:
            return False
