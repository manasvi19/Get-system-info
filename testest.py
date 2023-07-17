#!/usr/bin/env python
# coding: utf-8

import platform
import subprocess
import re


# Function to run a shell command and return the output
def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, _ = process.communicate()
    return output.decode('utf-8').strip()

# Function to get disk usage
def get_disk_usage():
    df_output = run_command('df -h')
    df_lines = df_output.split('\n')[1:]
    
    disk_usage = []
    for line in df_lines:
        parts = line.split()
        if len(parts) >= 5:
            filesystem = parts[0]
            size = parts[1]
            used = parts[2]
            available = parts[3]
            percentage_used = parts[4]
            # Handle the case when the percentage used is not in a recognized format
            try:
                percentage = float(percentage_used.strip('%'))
            except ValueError:
                percentage = 0.0
            disk_usage.append({
                'Filesystem': filesystem,
                'Size': size,
                'Used': used,
                'Available': available,
                'Percentage Used': percentage_used
            })
    
    return disk_usage

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
    os_manufacturer = platform.system()
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
    
    # Get disk usage
    disk_usage = get_disk_usage()
    most_used_disk = max(disk_usage, key=lambda x: float(x['Percentage Used'].strip('%')))
    system_info['Most Used Disk'] = most_used_disk

    # Get network interfaces
    network_interfaces = run_command('ifconfig -a')
    ip_addresses_output = run_command('ifconfig | grep "inet " | awk \'{print $2}\'')
    ip_addresses = ip_addresses_output.split('\n')
    system_info['IP Addresses'] = ip_addresses
    network_cards_output = run_command('networksetup -listallhardwareports')
    network_cards = network_cards_output.split('\n')
    formatted_network_cards = '\n'.join(network_cards)
    system_info['Network Cards'] = formatted_network_cards

    return system_info

# Get and print system information
system_info = get_system_info()
for key, value in system_info.items():
    print(f'{key}:\n{value}')
    print('-' * 50)
