import argparse


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-p",
        "--password",
        help="neocities password (can be set as $CITY_PASS)",
    )
    sp = ap.add_subparsers(dest="cmd", required=True)

    clonep = sp.add_parser("clone", help="clone a website into the current directory")
    clonep.add_argument("site_name")

    # keyp = sp.add_parser("key", help="print the API key for a site to stdout")
    # keyp.add_argument("-s", "--site", help="site name if not in .site_root")

    args = ap.parse_args()
    if args.cmd == "clone":
        from city.subcommands.clone import clone

        return clone(args)
    else:
        raise NotImplementedError()
