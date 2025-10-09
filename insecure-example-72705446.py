import paramiko
import paramiko.util
import json
import sys
import logging
from traceback import print_exc

config_file = sys.argv[1]
with open(config_file, r) as f:
    config = json.load(f)

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
