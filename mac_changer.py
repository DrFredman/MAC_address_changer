#!/usr/bin/env python

import subprocess
import optparse
import re
import sys
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac_address", dest="mac_address", help="MAC address to replace your existing MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface. Use --help for info.")
    elif not options.mac_address:
        parser.error("Please specify a MAC address. Use --help for info.")
    return options


def change_mac(interface, mac_address):
    print("[+] Changing MAC address for " + interface + " to " + mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_output = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_output))
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address as one does not exist for the interface you specified. Choose a different interface. ")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC: " + current_mac)
change_mac(options.interface, options.mac_address)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac_address:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed. ")