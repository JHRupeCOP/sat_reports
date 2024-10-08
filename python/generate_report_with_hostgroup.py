#!/usr/bin/env python3

import requests
import csv
import json
import getpass
from datetime import datetime

# API credentials
SATELLITE_URL = "https://satellite.conocophillips.net/"
CERT_PATH = "/etc/pki/tls/certs/ca-bundle.crt"

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Output file with date
OUTPUT_FILE = f"subscribed_hosts_report_{current_date}.csv"

# Function to fetch data from Satellite
def fetch_hosts_data():
    url = f"{SATELLITE_URL}/api/v2/hosts?per_page=1000"
    response = requests.get(url, auth=(username, password), verify=CERT_PATH)
    if response.status_code == 200:
        return response.json()['results']
    else:
        response.raise_for_status()

# Function to parse data and generate report
def generate_report(hosts_data):
    # Dictionary to hold counts
    counts = {}

    # Loop through each host
    for host in hosts_data:
        os_version = host['operatingsystem_name']
        location = host['location_name']
        host_group = host.get('hostgroup_name', 'N/A')  # 'N/A' if host group is missing

        # Create a key for the counts dictionary
        key = (os_version, location, host_group)

        # Increment the count for the key
        if key in counts:
            counts[key] += 1
        else:
            counts[key] = 1

    # Write counts to CSV
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["OS Version", "Location", "Host Group", "Count"])
        for key, count in counts.items():
            writer.writerow([key[0], key[1], key[2], count])

    print(f"Report generated: {OUTPUT_FILE}")

# Main function to run the script
def main():
    # Prompt for Satellite credentials
    username = input("Enter your Satellite username: ")
    password = getpass.getpass("Enter your Satellite password: ")

    try:
        # Fetch hosts data
        hosts_data = fetch_hosts_data()

        # Generate report
        generate_report(hosts_data)

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
