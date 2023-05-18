#!/usr/bin/env python3

import os
import shutil
import argparse
import importlib
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
import threading
import getpass
from diff import diff_files
# from config import (
#     DIRECTORY,
#     DEVICE_OBJECTS
# )

# Define a function to execute commands on a device and save the output to a file
def run_commands(ip, commands, choice):
    try:
        # Connect to the device using PyEZ
        dev = Device(host=ip, user=username, password=password, port=22, ssh_config=None)
        dev.open()

        # Create the output file path
        if not os.path.isdir(module.DIRECTORY):
            os.makedirs(module.DIRECTORY, exist_ok=True)

        filepath_pre = os.path.join(module.DIRECTORY,f'{ip}_pre.output')
        filepath_post = os.path.join(module.DIRECTORY,f'{ip}_post.output')

        if choice == 'p':
            with open(filepath_pre, 'w') as f:
                f.write('')
        elif choice == 'v':
            with open(filepath_post, 'w') as f:
                f.write('')

        # Run each command and save the output to a file named after the IP address
        for command in commands:
            output = dev.rpc.cli(command, format="text").text
            if choice == 'p':
                with open(filepath_pre, 'a') as f:
                    f.write(f'Command: {command}\n\n{output}\n\n')
            elif choice == 'v':
                with open(filepath_post, 'a') as f:
                    f.write(f'Command: {command}\n\n{output}\n\n')

        # Close the PyEZ connection
        dev.close()

    except ConnectError as err:
        print(f"Failed to connect to device {ip}: {err}")

# Define a function to execute commands on all devices in a group
def run_commands_on_group(devices, choice):
    # Loop through each device in the group and execute commands
    for device in devices:
        ips = device['ip']
        commands = device['commands']
        for ip in ips:
            t = threading.Thread(target=run_commands, args=(ip, commands, choice))
            t.start()

def run_diff_on_group(devices):
    for device in devices:
        ips = device['ip']
        for ip in ips:
            filepath_pre = os.path.join(module.DIRECTORY,f'{ip}_pre.output')
            filepath_post = os.path.join(module.DIRECTORY,f'{ip}_post.output')
            diff_files(filepath_pre, filepath_post)

def run_quit_task():
    if os.path.isdir(module.DIRECTORY):
        while True:
            response = input(f"Do you want to clean up all the files under '{module.DIRECTORY}' directory? (y/n) ")
            if response.lower() in ['yes', 'y']:
                try:
                    shutil.rmtree(module.DIRECTORY)
                    print(f"All files under '{module.DIRECTORY}' directory have been deleted.")
                except Exception as e:
                    print(f"Failed to delete files: {e}")
                break
            elif response.lower() in ['no', 'n']:
                print(f"All files under '{module.DIRECTORY}' directory have been kept.")
                break
            else:
                print(f"Invalid response: '{response}'. Please enter 'yes' or 'no'.")

# Loop through each group in the configuration file and execute commands in parallel

parser = argparse.ArgumentParser()
parser.add_argument("config", type=str, help="The name of the config file")
args = parser.parse_args()
module = importlib.import_module(args.config)
# print(module.DIRECTORY)
# print(module.DEVICE_OBJECTS)

while True:
    print("Choose from following:")
    print("[P]re-check")
    print("[V]erification")
    print("[D]iff")
    print("[Q]uit")
    choice = input("Enter your choice (P/V/D/Q): ").lower()

    if choice == 'p' or choice == 'v':
        # Prompt the user to input the username and password
        username = input("Enter your RIMNET username: ")
        password = getpass.getpass("Enter the password: ")
        for device_type, devices in module.DEVICE_OBJECTS.items():
            run_commands_on_group(devices, choice)
    elif choice == 'd':
        for device_type, devices in module.DEVICE_OBJECTS.items():
            run_diff_on_group(devices)
    elif choice == 'q':
        run_quit_task()
        break
    else:
        print("\nInvalid choice. Please enter 'P', 'V', 'D' or 'Q'.\n")