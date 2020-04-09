#!/usr/bin/env python3

# Import local configuration

import os
import re
import time
import argparse
import subprocess

def is_root():
    return os.getuid() == 0

def get_privileges():
    if not is_root():
        import elevate
        print("Not running as root, elevating.")
        elevate.elevate(graphical=False)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="client_id from Spotify auth API")
    parser.add_argument("--secret", help="client_secret from Spotify auth API")

    return parser.parse_args()

def write_config(id, secret):
    from config import config # Config needs to be loaded here, otherwise elevating
    # privileges causes config to be lost

    f = open(config['mopidy']['config_file'], "r")
    mopidy_config = f.read()
    f.close()

    f = open(config['mopidy']['config_file'], "w")

    mopidy_config = re.sub(r'client_id = .+?\n', "client_id = {}\n".format(id), mopidy_config)
    mopidy_config = re.sub(r'client_secret = .+?\n', "client_secret = {}\n".format(secret), mopidy_config)

    f.write(mopidy_config)
    f.close()

    return config

def restart_mopidy():
    time.sleep(2)
    subprocess.run(['systemctl', 'restart', 'mopidy.service'])

def main():
    get_privileges()
    args = parse_arguments()
    write_config(args.id, args.secret)
    restart_mopidy()

main()
