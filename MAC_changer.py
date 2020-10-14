#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="iface", help="The interface you want to change the MAC address for")
    parser.add_option('-m', '--mac', dest="new_mac", help="The new MAC address you want to put in your network interface")
    print("[+] Parsing input...")
    return parser.parse_args()


def spoofer(iface, spoofed_mac):
    print("[+] Changing MAC address to " + new_mac + "...")
    subprocess.call("ifconfig " + iface + " down", shell=True)
    subprocess.call("ifconfig " + iface + " hw " + "ether " + spoofed_mac, shell=True)
    subprocess.call("ifconfig " + iface + " up", shell=True)
    ifconfig_output = subprocess.check_output(["ifconfig", iface])
    filtered_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
    print(filtered_mac.group(0))
    print("[+] Your MAC address changed successfully. Ready to attack!")


(options, arguments) = get_arguments()
iface = options.iface
new_mac = options.new_mac

spoofer(options.iface, options.new_mac)