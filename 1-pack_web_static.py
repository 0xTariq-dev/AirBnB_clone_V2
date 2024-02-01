#!/usr/bin/python3
# Script that generates a .tgz archive from the contents of the web_static
from fabric.api import local
from datetime import datetime
from os import path


def do_pack():
    """Function to pack web_static directory into a .tgz archive """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(timestamp)
    print(f"Packing web_static to versions/web_static_{timestamp}.tgz")

    if not path.isdir("versions"):
        if local("mkdir -p versions").failed is True:
            return None

    return None if local(f"tar -cvzf {file} web_static").failed else file
