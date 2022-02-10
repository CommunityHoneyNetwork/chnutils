import argparse
import uuid
from chn_utils.hpfeeds_user import create_user


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongodb-host", required=True)
    parser.add_argument("--mongodb-port", required=True, type=int)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--ident", required=True)
    parser.add_argument("--secret", required=False, default="")
    parser.add_argument("--publish", required=True)
    parser.add_argument("--subscribe", required=True)
    args = parser.parse_args()

    host = args.mongodb_host
    port = args.mongodb_port

    owner = args.owner
    ident = args.ident
    publish = args.publish
    subscribe = args.subscribe
    if args.secret:
        secret = args.secret
    else:
        secret = str(uuid.uuid4()).replace("-", "")

    res, rec = create_user(host=host, port=port, owner=owner, ident=ident,
                           secret=secret, publish=publish, subscribe=subscribe)

    if res['updatedExisting']:
        print("updated %s" % rec)
    else:
        print("inserted %s" % rec)


if __name__ == "__main__":
    main()
