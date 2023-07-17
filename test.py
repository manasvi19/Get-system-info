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
                'Size': size,
                'Used': used,
                'Available': available
            })
    return disk_usage


# Function to get network cards and their IP addresses
def get_network_cards():
    network_cards_output = run_command('networksetup -listallhardwareports')
    network_cards_lines = network_cards_output.split('\n')
    network_cards = []
    for line in network_cards_lines:
        if line.startswith('Hardware Port:'):
            network_card = line.split(':')[1].strip()
            network_cards.append(network_card)
    
    ip_addresses_output = run_command('ifconfig | grep "inet " | awk \'{print $2}\'')
    ip_addresses = ip_addresses_output.split('\n')
    
    return network_cards, ip_addresses

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
    
    # Get disk usage information
    disk_usage = get_disk_usage()
    system_info['Disk Usage'] = disk_usage

    # Get network cards and their IP addresses
    network_cards, ip_addresses = get_network_cards()
    system_info['Network Cards'] = network_cards
    system_info['IP Addresses'] = ip_addresses

    return system_info

# Get and print system information
system_info = get_system_info()
for key, value in system_info.items():
    print(f'{key}:')
    if key == 'Disk Usage':
        for disk in value:
            print(f'Used: {disk["Used"]}')
            print(f'Available: {disk["Available"]}')
            print('-' * 50)
    else:
        print(value)
        print('-' * 50)
