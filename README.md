# Python Linux MAC Changer 1.0.0

## What is this script?

This is a simple MAC address changer created for Linux systems.


## Commented code
There is one .py file with the code fully commented (for educational purposes) and another .py file that contains only the code with necessary comments.


## How to use the script?

The user can chose which interface he wants to change the MAC address (-i, --interface) and then provide the desired MAC address (-m, --mac). Still, the user has the option to use a random generated MAC address provided by the script (-r, --random). If the user don't pass any arguments, the script will ask for the user to input the peding information. The script needs to be run with sudo or as root.

Example 1 - Specifing the interface and the MAC address: 
```
sudo ./linuxmacchanger.py -i eth0 -m 00:11:22:33:44:55
```
Example 2 - Specifing only that the user wants a random generated MAC address
```
sudo ./linuxmacchanger.py -r
```
