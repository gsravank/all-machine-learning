#!/usr/bin/env python

import os
import time
from optparse import OptionParser


def get_ip_port(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    return lines[0].strip()


def run_notebook():
    log_file = 'nb.log'
    cmd = "jupyter lab --NotebookApp.iopub_data_rate_limit=1.0e10 --port=8888 --no-browser --ip=0.0.0.0 > {} 2>&1 &".format(log_file)
    os.system(cmd)

    return log_file


def read_token_from_log(log_file):
    with open(log_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if 'http://' in line:
            return line.strip().split('token=')[-1]

def main(ip_port_file):
    # if not os.path.isfile(ip_port_file):
    #     print("Provide valid file with IP and Port details")
    #     return

    # Get IP and Port
    # try:
    #     ip_port = get_ip_port(ip_port_file)
    # except Exception:
    #     print("Could not read IP and Port details from file - {}".format(ip_port_file))
    #     print("Provide file containing text as 'IP:PORT' like '111.11.11.11:9999'")
    #     return

    # Run jupyter notebook
    log_file = run_notebook()
    time.sleep(10)

    # Read url from log
    token = read_token_from_log(log_file)
    print("Token: {}".format(token))

    # Print modified url
    # modified_url = 'http://{}/?token={}'.format(ip_port, token)
    # modified_url = 'http://{}/?token={}'.format(ip_port, token)
    # print("Open below URL to access jupyter notebook..")
    # print("     {}     ".format(modified_url))
    return


def ParseCommandlineArgs():
    parser = OptionParser()
    parser.add_option("-i", "--ipportfile", dest="ipportfile", default=os.path.join(os.getenv("HOME"), 'configs/data/ipport.txt'))
    
    options, _ = parser.parse_args()

    return options


if __name__ == "__main__":
    options = ParseCommandlineArgs()
    main(options.ipportfile)
