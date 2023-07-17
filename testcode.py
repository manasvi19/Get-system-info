#!/usr/bin/env python
# coding: utf-8

import platform
import subprocess


# Function to run a shell command and return the output
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode('utf-8').strip()

# Get system information
def get_system_info():
    system_info = {}
    
    # Get host name
    host_name = run_command('scutil --get ComputerName')
    system_info['Host Name'] = host_name
    
    # Get operating system information
    os_name = platform.system()
    os_version = platform.mac_ver()[0]
    os_build = run_command('sw_vers -buildVersion')
    #os_manufacturer = "Apple"
    os_manufacturer = platform.system()
    print("OS Manufacturer:", os_manufacturer)
    system_info['OS Name'] = os_name
    system_info['OS Version'] = os_version
    system_info['OS Build'] = os_build
    system_info['OS Manufacturer'] = os_manufacturer
    
    # Get processor information
    processor_name = run_command('sysctl -n machdep.cpu.brand_string')
    system_info['Processor'] = processor_name
    
    # Get memory information
    memory_info = run_command('sysctl -n hw.memsize')
    system_info['Memory'] = memory_info
    
    # Get disk information
    disk_info = run_command('diskutil list')
    system_info['Disk Information'] = disk_info
    
    # Get network interfaces
    network_interfaces = run_command('ifconfig -a')
    ip_addresses_output = run_command('ifconfig | grep "inet " | awk \'{print $2}\'')
    ip_addresses = ip_addresses_output.split('\n')
    system_info['IP Addresses'] = ip_addresses
    network_cards_output = run_command('networksetup -listallhardwareports')
    network_cards = network_cards_output.split('\n')
    formatted_network_cards = []
    is_vlan_section = False
    for line in network_cards:
        if line.strip() == "VLAN Configurations":
            is_vlan_section = True
        elif not is_vlan_section:
            formatted_network_cards.append(line)
        
        formatted_network_cards = '\n'.join(formatted_network_cards)
        system_info['Network Cards'] = formatted_network_cards

    
    #network_cards_output = run_command('networksetup -listallhardwareports')
    #network_cards = network_cards_output.split('\n')
    #system_info['Network Cards'] = network_cards
    
    
    
    # Get graphics information
    graphics_info = run_command('system_profiler SPDisplaysDataType')
    system_info['Graphics Information'] = graphics_info

    
    return system_info

# Get and print system information
system_info = get_system_info()
for key, value in system_info.items():
    print(f'{key}:')
    print(value)
    print('-' * 50)
