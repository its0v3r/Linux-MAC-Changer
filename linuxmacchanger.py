#!/usr/bin/env python
#
# PYTHON LINUX MAC CHANGER
#
# Author: Matheus Heidemann
#
# Description: this is a simple MAC address changer created for Unix systems. The user can chose which interface he wants to change the MAC address
# (-i, # --interface) and then provide the desired MAC address (-m, --mac). Still, the user has the option to use a random generated MAC address
# provided by the # script. If the user don't pass any arguments, the script will ask for the user to input the peding information.
#
# 22 July 2022
#
# Version: 1.0.0
#
# License: MIT License
#
#
#
# Imports
import argparse
import random
import re
import string
import subprocess
import os
from time import sleep

# Regex pattern to validate the MAC address
valid_mac_pattern = "^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$"

# Function to check if the user has runned the script as sudo or root


def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        print("You need to run this script with sudo or as root.")
        quit()


# Function to generate a random MAC address
def generate_random_mac_address():
    # Generates 12 scrambled hexadecimal digits
    # Set is used to generate a collection of non-ordened digits
    # Join is used to join each value from the set in a single string
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))

    # Define a empty variable for the random MAC address
    mac = ""

    # Loop will happen 6 times in index1, where which time in index1, index2 loop will happen 2 times
    for index1 in range(6):
        for index2 in range(2):
            # If it is the 2nd index2 loop
            if index2 == 0:
                # Attribute any value from the hexdigits to the MAC address
                mac += random.choice(uppercased_hexdigits)
            # If it is the 1st index2 loop
            elif index2 == 1:
                # Attribute a value (0, 2, 4, 6, 8, A, C, E)
                mac += random.choice("02468ACE")

        # After define 2 digits, insert a :
        mac += ":"

    # Return the random MAC address, but removing the : after the final digit
    return mac.strip(":")


# Function to get the current MAC address
def get_current_mac():
    # Calls the "ip link show" command and decodes his output as an string
    output = subprocess.check_output("ip link show", shell=True).decode()

    # Use regex to return the current MAC address
    return re.search("ether (.+) ", output).group().split()[1].strip()


# Function to define the argparser arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="PYTHON LINUX MAC CHANGER - Script to change MAC address on Linux systems")
    parser.add_argument("-i", "--interface", help="Network interface that will have it's MAC address changed")
    parser.add_argument("-m", "--mac", help="The new MAC address that the defined interface will receive")
    parser.add_argument("-r", "--random", action="store_true", help="Generates a random MAC address")

    # Pass the defined arguments to the parser from argparse
    args = parser.parse_args()

    # Get all avaliable interface
    avaliable_interfaces = (subprocess.check_output("ip -o link show | awk -F':' '{printf \"%s%s\",sep,$2; sep=\",\"}'", shell=True).decode()).strip().replace(" ", "")
    print("Avaliable interfaces: " + str(avaliable_interfaces).strip("[]").replace("'", "").replace(",", ", "))
    print("")

    # Create a list with all avaliable interfaces
    avaliable_interfaces = avaliable_interfaces.split(",")

    # Variable used to check if the interface provided was already checked
    interface_not_checked = True

    # Dealing with the interface value
    while True:
        # If the interface wasn't defined or if the interface is not on the "avaliable_interfaces" list
        if not args.interface or args.interface not in avaliable_interfaces:
            # Show an error only if the first defined interface value (got from the -i/--interface argument) is not avaliable
            if args.interface and interface_not_checked == True:
                print(f"ERROR - The interface [{args.interface}] is not avaliable.")
                interface_not_checked = False

            # Asks for the user to input an interface name
            args.interface = input("Interface > ")
            print("")

            # Set the "interface_not_checked" to False
            interface_not_checked = False

        # If the provided interface name is on the "avaliable_interfaces" list
        if args.interface in avaliable_interfaces:
            print(f"Selected interface: [{args.interface}]")
            print("")
            break

        # If the provided interface name is not on the "avaliable_interfaces" list
        print(f"ERROR - The interface [{args.interface}] is not avaliable.")
        print("Avaliable interfaces: " + str(avaliable_interfaces).strip("[]").replace("'", "").replace(", ", ", "))

    # Dealing with the MAC address value
    # If no MAC address value was passed as an argument
    if not args.mac:
        # If the user didn't specified if he wants an random MAC address with the "-r/--random" argument
        if not args.random:
            # Asks if the user want the script to generate an random MAC address
            generate_random = input("Você deseja gerar um endereço MAC aleatório?[Y,n] ") or "Y"

        # If the user wants the script to generate an random MAC address
        if args.random or generate_random.upper() == "Y":
            args.mac = generate_random_mac_address()
            print(f"Your random MAC address is: {args.mac}")

        # IF the user doesn't want the script to generate an random MAC address
        else:
            while True:
                # Asks the user to input a valid MAC address
                args.mac = input("Endereço MAC > ")

                # If the provided MAC address is invalid
                if not re.match(valid_mac_pattern, args.mac):
                    print("ERRO - Endereço MAC inválido.")

                # If the provided MAC address is the same as the current MAC address
                if args.mac.upper() == old_mac.upper():
                    print("ERRO - Endereço MAC inserido é igual ao endereço MAC atual.")

                # If the provided MAC address is valid and it's not the same as the current MAC address
                if re.match(valid_mac_pattern, args.mac) and not args.mac.upper() == old_mac.upper():
                    break

    # Return the defined arguments
    return args


# Function to change the MAC address
def change_mac(interface, new_mac):
    print("")
    print(f"Changing the MAC address from the interface [{interface}] to {new_mac}")

    # Call the commands to change the MAC address
    subprocess.call(["ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", "dev", interface, "up"])

    # Processing changes
    print("Processing changes...")
    print("")

    # Print that the script succeded to change the MAC address and then print the interface, the old MAC address and the new MAC address
    print("SUCCESS!")
    print(f"[{interface}] You old MAC address was {old_mac.upper()} and your new MAC address is {new_mac}")


# DEFAULT FUNCTION CALLS
# Check user privileges
check_privileges()

# Store the old MAC address
old_mac = get_current_mac()

# Get the arguments
args = get_arguments()

# Change the MAC address
change_mac(args.interface, args.mac)
