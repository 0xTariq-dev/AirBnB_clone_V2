#!/usr/bin/python3
# Script that generates a .tgz archive from the contents of the web_static
from fabric.api import *
from fabric.decorators import runs_once
from datetime import datetime
from os.path import isfile, isdir, getsize

env.hosts = ["100.26.173.229", "35.153.66.163"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/school"


@runs_once
def do_pack():
    """Function to pack web_static directory into a .tgz archive """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(timestamp)
    print(f"Packing web_static to versions/web_static_{timestamp}.tgz")

    if not isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    if local(f"tar -cvzf {file} web_static/*").succeeded:
        file_size = getsize(file)
        print(f"web_static packed: {file} -> {file_size} bytes")
        return file
    else:
        return None


def do_deploy(archive_path):
    """Function to deploy the web_static archive to the servers
    Args:
        archive_path: path to the archive to deploy

    Returns:
        False if the file at the path archive_path doesn't exist.
    """
    if not isfile(archive_path):
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]
    path = "/data/web_static/releases/"

    try:
        put(archive_path, '/tmp/')
        run("rm -rf {}{}".format(path, name))
        run("mkdir -p {}{}".format(path, name))
        run("tar -xzf /tmp/{} -C {}{}".format(file, path, name))
        run("rm -f /tmp/{}".format(file))
        run("rm -rf /data/web_static/current")
        run("mv {}{}/web_static/* {}{}".format(path, name, path, name))
        run("rm -rf {}{}/web_static".format(path, name))
        run("ln -sf {}{} /data/web_static/current".format(path, name))
        sudo("service nginx restart")
        return True
    except Exception as e:
        return False


def deploy():
    """Function to deploy the web_static archive to the servers."""
    archive = do_pack()
    if archive is None:
        return False

    return do_deploy(archive)
