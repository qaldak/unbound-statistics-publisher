from python_on_whales import docker

import subprocess

def get_metrics():
    # metrics = docker.execute("unbound_manjarows", "/opt/unbound/sbin/unbound-control stats_noreset", stream=True)
    metrics = docker.execute("unbound_manjarows", "echo $USER", tty=True, interactive=True)
    # sub_cmd = "docker exec -i unbound_manjarows unbound-control stats_noreset"
    # metrics = subprocess.check_output(sub_cmd, shell=True)
    print(metrics)


get_metrics()