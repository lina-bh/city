import os
import sys
from getpass import getpass


def get_password():
    try:
        password = os.environ["CITY_PASS"]
    except KeyError:
        password = getpass()
        print("consider exporting $CITY_PASS as your password", file=sys.stderr)
    return password
