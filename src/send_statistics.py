from python_on_whales import docker, DockerException


def send_metrics(metrics, receiver=str()):
    try:
        docker.run("busybox", ["echo", metrics], remove=True)
        print("foo")
    except DockerException as e:
        print(e)


send_metrics("Foo")
print(docker.context)
