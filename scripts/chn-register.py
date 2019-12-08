#!/usr/bin/env python3

import sys
import json
import argparse
import socket
import requests


def parse_args():
    parser = argparse.ArgumentParser(description='Register sensor to CHN server')
    parser.add_argument('-p', '--honeypot', help='Type of honeypot for this sensor', required=True)
    parser.add_argument('-d', '--deploy-key', help='Deploy Key for registration', required=True)
    parser.add_argument('-n', '--hostname', help='Hostname of honeypot', default=socket.gethostname())
    parser.add_argument('-i', '--ip-address', help='IP of honeypot', default=socket.gethostbyname(socket.gethostname()))
    parser.add_argument('-u', '--url', help='CHN Server to register to', required=True)
    parser.add_argument('-k', '--no-verify', help='Do not verify TLS connection', action='store_true')
    parser.add_argument('-o', '--state-output', help='State output file', type=argparse.FileType('w'))

    return parser.parse_args()

def main():

    args = parse_args()
    name = "%s-%s" % (args.hostname, args.honeypot)
    resp = requests.post(
               "%s/api/sensor/" % args.url,
               headers={
                   "Content-Type": "application/json"
               },
               json={
                   "name": name,
                   "deploy_key": args.deploy_key,
                   "hostname": args.hostname,
                   "ip": args.ip_address,
                   "honeypot": args.honeypot,
               },
               verify=not args.no_verify
    )
    try:
        resp.raise_for_status()
    except Exception as e:
        logging.error("Could not register client ☹️")
        logging.error("%s" % e)
        return 5

    args.state_output.write(json.dumps(resp.json()))
    return 0

if __name__ == "__main__":
    sys.exit(main())
