#!/usr/bin/env python3

import json
import sys

try:
    import requests
except ImportError:
    print("Please install the python-requests module.")
    sys.exit(-1)

SAT = "bvlusatp0001.conocophillips.net"
# URL for the API to your deployed Satellite 6 server
SAT_API = f"https://{SAT}/api/"
KATELLO_API = f"https://{SAT}/katello/api/v2/"

POST_HEADERS = {'content-type': 'application/json'}
# Default credentials to login to Satellite 6
USERNAME = "ruppej"
PASSWORD = "Ultimate4592Sin!"
# Ignore SSL for now
# SSL_VERIFY = False
SSL_VERIFY = "/etc/pki/tls/certs/ca-bundle.crt"


def get_json(url):
    # Performs a GET using the passed URL location
    r = requests.get(url, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)
    return r.json()

def get_results(url):
    jsn = get_json(url)
    if jsn.get('error'):
        print("Error: " + jsn['error']['message'])
    else:
        if jsn.get('results'):
            return jsn['results']
        elif 'results' not in jsn:
            return jsn
        else:
            print("No results found")
    return None

def display_all_results(url):
    results = get_results(url)
    if results:
        print(json.dumps(results, indent=4, sort_keys=True))

def display_info_for_hosts(url):
    hosts = get_results(url)
    if hosts:
        print(f"{'ID':10}{'Name':40}{'IP':30}{'Operating System':30}")
        for host in hosts:
            print(f"{str(host['id']):10}{host['name']:40}{str(host['ip']):30}{str(host['operatingsystem_name']):30}")

def display_info_for_subs(url):
    subs = get_results(url)
    if subs:
        print(f"{'ID':10}{'Name':90}{'Start Date':30}")
        for sub in subs:
            print(f"{str(sub['id']):10}{sub['name']:90}{str(sub['start_date']):30}")

def main():
    host = SAT
    print(f"Displaying all info for host {host} ...")
    display_all_results(SAT_API + 'hosts/' + host)

    print(f"Displaying all facts for host {host} ...")
    display_all_results(SAT_API + f'hosts/{host}/facts')

    host_pattern = 'example'
    print(f"Displaying basic info for hosts matching pattern '{host_pattern}'...")
    display_info_for_hosts(SAT_API + 'hosts?per_page=1&search=name~' + host_pattern)

    print(f"Displaying basic info for subscriptions")
    display_info_for_subs(KATELLO_API + 'subscriptions')

    environment = 'production'
    print(f"Displaying basic info for hosts in environment {environment}...")
    display_info_for_hosts(SAT_API + 'hosts?search=environment=' + environment)


if __name__ == "__main__":
    main()
