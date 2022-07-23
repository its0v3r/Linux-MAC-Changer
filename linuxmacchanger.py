#!/usr/bin/env python
#
# IMPORTS
import argparse
import random
import re
import string
import subprocess
import os
from time import sleep

# MISC
valid_mac_pattern = "^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$"


# FUNCTIONS
# Function to check if the user has runned the script as sudo or root
def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        print("You need to run this script with sudo or as root.")
        quit()


# Function to generate a random MAC address
def generate_random_mac_address():
    uppercased_hexdigits = ''.join(set(string.hexdigits.upper()))
    mac = ""
    for index1 in range(6):
        for index2 in range(2):
            if index2 == 0:
                mac += random.choice(uppercased_hexdigits)
            elif index2 == 1:
                mac += random.choice("02468ACE")
        mac += ":"
    return mac.strip(":")


# Function to get the current MAC address
def get_current_mac():
    output = subprocess.check_output("ip link show", shell=True).decode()
    return re.search("ether (.+) ", output).group().split()[1].strip()


# Function to define the argparser arguments
def get_arguments():
    parser = argparse.ArgumentParser(description="PYTHON LINUX MAC CHANGER - Script to change MAC address on Linux systems")
    parser.add_argument("-i", "--interface", help="Network interface that will have it's MAC address changed")
    parser.add_argument("-m", "--mac", help="The new MAC address that the defined interface will receive")
    parser.add_argument("-r", "--random", action="store_true", help="Generates a random MAC address")
    args = parser.parse_args()

    avaliable_interfaces = (subprocess.check_output("ip -o link show | awk -F':' '{printf \"%s%s\",sep,$2; sep=\",\"}'", shell=True).decode()).strip().replace(" ", "")

    print("Avaliable interfaces: " + str(avaliable_interfaces).strip("[]").replace("'", "").replace(",", ", "))
    print("")

    avaliable_interfaces = avaliable_interfaces.split(",")
    interface_not_checked = True

    while True:
        if not args.interface or args.interface not in avaliable_interfaces:
            if args.interface and interface_not_checked == True:
                print(f"ERROR - The interface [{args.interface}] is not avaliable.")
                interface_not_checked = False

            args.interface = input("Interface > ")
            print("")

            interface_not_checked = False

        if args.interface in avaliable_interfaces:
            print(f"Selected interface: [{args.interface}]")
            print("")
            break

        print(f"ERROR - The interface [{args.interface}] is not avaliable.")
        print("Avaliable interfaces: " + str(avaliable_interfaces).strip("[]").replace("'", "").replace(", ", ", "))

    if not args.mac:
        if not args.random:
            generate_random = input("Você deseja gerar um endereço MAC aleatório?[Y,n] ") or "Y"
        if args.random or generate_random.upper() == "Y":
            args.mac = generate_random_mac_address()
            print(f"Your random MAC address is: {args.mac}")
        else:
            while True:
                args.mac = input("Endereço MAC > ")
                if not re.match(valid_mac_pattern, args.mac):
                    print("ERRO - Endereço MAC inválido.")
                if args.mac.upper() == old_mac.upper():
                    print("ERRO - Endereço MAC inserido é igual ao endereço MAC atual.")
                if re.match(valid_mac_pattern, args.mac) and not args.mac.upper() == old_mac.upper():
                    break
    return args


# Function to change the MAC address
def change_mac(interface, new_mac):
    print("")
    print(f"Changing the MAC address from the interface [{interface}] to {new_mac}")

    subprocess.call(["ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["ip", "link", "set", "dev", interface, "up"])

    print("Processing changes...")
    print("")
    print("SUCCESS!")
    print(f"[{interface}] You old MAC address was {old_mac.upper()} and your new MAC address is {new_mac}")


# PROGRAM
check_privileges()
old_mac = get_current_mac()
args = get_arguments()
change_mac(args.interface, args.mac)
