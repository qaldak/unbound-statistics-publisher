from python_on_whales import docker


class Container:
    def __init__(self, name):
        self.name = name

    def _check_container(self):
        return docker.ps(filters={"name": self.name})

    def is_running(self):
        container_found = self._check_container()

        if container_found:
            for container in self._check_container():
                # Todo: logger
                print(type(container))
                print(container)
                if container.state.status == "running":
                    return True
                else:
                    return False
        else:
            # Todo: logger
            return False
