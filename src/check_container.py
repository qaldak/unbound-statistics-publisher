from python_on_whales import docker, DockerException, ClientNotFoundError


class Container:
    def __init__(self, name):
        self.name = name

    def is_running(self):
        container_found = self.call_container()

        if container_found:
            for container in self.call_container():
                # Todo: logger
                print(type(container))
                print(container)
                # print(f"Container is {container.state}")
                if container.state.status == "running":
                    return True
                else:
                    return False
        else:
            print(f"Container '{self.name}' not found")
            return False

    def call_container(self):
        return docker.ps(all, filters={"name": self.name})


if Container("busybox").is_running():
    print("foo")
else:
    print("bar")
