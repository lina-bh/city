import hashlib
import os
import os.path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from datetime import datetime

import dateutil.parser
from dateutil.tz import tzutc

from city.http import sess
from city.api.common import BASE_URI, Failure


@dataclass(unsafe_hash=True)
class File:
    path: str
    is_directory: bool
    # size = int
    updated_at: datetime
    sha1_hash: Optional[bytes]

    @classmethod
    def from_json(cls, d: dict):
        sha1_hash = d.get("sha1_hash")
        if sha1_hash:
            sha1_hash = bytes.fromhex(sha1_hash)
        return cls(
            d["path"],
            d["is_directory"],
            dateutil.parser.parse(d["updated_at"]),
            sha1_hash,
        )


def remote_list(auth) -> List[File]:
    req = sess.get(BASE_URI + "/list", auth=auth)
    req.raise_for_status()
    o = req.json()
    if o["result"] != "success":
        raise Failure()
    fs = [File.from_json(f) for f in o["files"]]
    return fs


from pprint import pprint


def hash_file(path):
    size = 2048
    hasher = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            d = f.read(size)
            hasher.update(d)
            if len(d) == 0:
                break
    return hasher.digest()


def local_list(root_path, hash_files=False):
    paths = []
    for (p, ds, fs) in os.walk(root_path):
        for f in fs + ds:
            paths.append((p + "/" + f)[2:])
    return [
        File(
            p,
            False,
            datetime.fromtimestamp(int(os.path.getmtime(p)), tzutc()),
            hash_file(p) if hash_files else None,
        )
        if os.path.isfile(p)
        else File(
            p, True, datetime.fromtimestamp(int(os.path.getctime(p)), tzutc()), None
        )
        for p in paths
    ]
