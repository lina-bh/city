import os
import sys
import time

import requests

from city.api.list import remote_list
from city.auth import get_password
from city.http import download_file


def write_site_root(site_name):
    with os.fdopen(
        os.open(".site_root", os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode=0o666), "w"
    ) as f:
        f.write(site_name + "\n")


def clone(args) -> int:
    site_name = args.site_name
    if len(os.listdir()) != 0:
        print("current directory needs to be empty", file=sys.stderr)
        return 1

    if args.password:
        password = args.password
    else:
        password = get_password()
    site_base = f"https://{site_name}.neocities.org/"
    fs = remote_list((site_name, password))
    for f in fs:
        if f.is_directory:
            os.mkdir(f.path)
            ts = f.updated_at.timestamp()
            os.utime(f.path, (time.time(), ts))
        else:
            print("downloading", f.path, file=sys.stderr)
            download_file(site_base, f.path, f.updated_at)
    write_site_root(site_name)
    print("done", file=sys.stderr)
    return 0
