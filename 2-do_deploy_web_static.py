#!/usr/bin/python3
# Script that generates a .tgz archive from the contents of the web_static
from fabric.api import local, env, put, run
from os import path

env.hosts = ["100.26.173.229", "54.172.48.37"]


def do_deploy(archive_path):
    """Function to deploy the web_static archive to the servers
    Args:
        archive_path: path to the archive to deploy

    Returns:
        False if the file at the path archive_path doesn't exist.
    """
    # do_pack()
    if not path.isfile(archive_path):
        return False
    
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    
    commands = [
        f"rm -rf /data/web_static/releases/{name}/",
        f"mkdir -p /data/web_static/releases/{name}/",
        f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/",
        f"rm /tmp/{file}",
        f"mv /data/web_static/releases/{name}/web_static/* "
        f"/data/web_static/releases/{name}/",
        f"rm -rf /data/web_static/releases/{name}/web_static",
        f"rm -rf /data/web_static/current",
        f"ln -s /data/web_static/releases/{file}/ /data/web_static/current"
    ]

    put(archive_path, f'/tmp/{file}')
    for command in commands:
        if run(command).failed is True:
            return False

    return True    

