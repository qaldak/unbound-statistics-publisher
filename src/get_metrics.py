from python_on_whales import docker


def get_metrics():
    container_list = docker.ps(all, filters={"name": "opensearch-opensearch-1"})
    print(container_list)

