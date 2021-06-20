import functools
import os
import shutil
from datetime import datetime

import requests

sess = requests.Session()


def download_file(base, path, updated: datetime):
    with requests.get(base + path, stream=True) as r:
        r.raw.read = functools.partial(r.raw.read, decode_content=True)
        with open(path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    ts = updated.timestamp()
    os.utime(path, (ts, ts))
