#!/usr/bin/python3
# Script that generates a .tgz archive from the contents of the web_static
from fabric.api import local, env, put, run
from datetime import datetime
from os.path import isfile, isdir

env.hosts = ["100.26.173.229", "54.172.48.37"]


def do_pack():
    """Function to pack web_static directory into a .tgz archive """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(timestamp)
    print(f"Packing web_static to versions/web_static_{timestamp}.tgz")

    if not isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    return None if local(f"tar -cvzf {file} web_static").failed else file


def do_deploy(archive_path):
    """Function to deploy the web_static archive to the servers
    Args:
        archive_path: path to the archive to deploy

    Returns:
        False if the file at the path archive_path doesn't exist.
    """
    # do_pack()
    if not isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    path = "/data/web_static/releases/"

    try:
        put(archive_path, f'/tmp/{file}')
        run(f"rm -rf {path}{name}/")
        run(f"mkdir -p {path}{name}/")
        run(f"tar -xzf /tmp/{file} -C {path}{name}/")
        run(f"rm /tmp/{file}")
        run(f"mv {path}{name}/web_static/* {path}{name}/")
        run(f"rm -rf {path}{name}/web_static")
        run(f"rm -rf /data/web_static/current")
        run(f"ln -s {path}{file}/ /data/web_static/current")
        return True
    except:
        return False
