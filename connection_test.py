import paramiko
import paramiko.util
import json
import sys
import logging
from traceback import print_exc

log_file = "paramiko-debug.log"
logging.basicConfig(filename=log_file, filemode="a", level=logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',\
                     datefmt = '%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
paramiko.util.log_to_file("otherlog.log")

config_file = sys.argv[1]
logging.debug(f"Using config file: {config_file}")
with open(config_file, 'r') as f:
    config = json.load(f)

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    hostname = config.get("host")
    port = config.get("port", 22)
    username = config.get("username")
    password = config.get("password", "")
    key_path = config.get("key_path", "")
    key_passphrase = config.get("key_passphrase", "")
    disable_rsa2 = config.get("disable_rsa2", False)

    if key_path != "" and not disable_rsa2:
        try:
            logging.debug("Trying to connect with key.")
            client.connect(hostname, port, username, key_filename=key_path, passphrase=key_passphrase, timeout=20)
            logging.debug("Connected using key.")
        except Exception as e:
            logging.error("Connection with key failed.")
            logging.exception(e)
    elif key_path != "" and disable_rsa2:
        try:
            client.connect(hostname, port, username, key_filename=key_path, passphrase=key_passphrase, disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]), timeout=20)
            logging.debug("Connected with key and disabled algorithms.")
        except Exception as e:
            logging.error("Connection with key and disabled algorithms still failed.")
            logging.exception(e)
    elif username != "":
        try:
            logging.debug("Trying to connect with password.")
            client.connect(hostname, port, username, password, timeout=20)
            logging.debug("Connected with password.")
        except Exception as e:
            logging.error("Unable to connect with password.")
            logging.exception(e)

    logging.info("Closing client.")
    client.close()