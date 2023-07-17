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
    print("OS Manufacturer:", os_manufacturer)
    system_info['OS Name'] = os_name
    system_info['OS Version'] = os_version
    system_info['OS Build'] = os_build
    system_info['OS Manufacturer'] = os_manufacturer
    
    # Get processor information
    processor_name = run_command('sysctl -n machdep.cpu.brand_string')
    system_info['Processor'] = processor_name
    
    # Get memory information
    total_memory_output = run_command('sysctl -n hw.memsize')
    total_memory_bytes = int(total_memory_output)
    total_memory_gb = round(total_memory_bytes / (1024 ** 3), 2)
    system_info['Total Memory'] = f'{total_memory_gb} GB'
    
    available_memory_output = run_command('sysctl -n hw.memsize')
    available_memory_bytes = int(available_memory_output)
    available_memory_gb = round(available_memory_bytes / (1024 ** 3), 2)
    system_info['Available Memory'] = f'{available_memory_gb} GB'
    
    # Get disk information
    def get_disk_info():
    disk_info = []
    
        # Get disk list
        disk_list_output = run_command('diskutil list')
        disk_list_lines = disk_list_output.split('\n')
        
        # Find the disks with their sizes
        for line in disk_list_lines:
            if 'disk' in line:
                line_parts = line.split()
                if len(line_parts) > 3:
                    disk_name = line_parts[0]
                    disk_size = line_parts[2]
                    disk_info.append(f"Disk {disk_name}: Size {disk_size}")
        
        return disk_info
    
        # Get and print disk information
        disk_info = get_disk_info()
        for disk in disk_info:
            print(disk)

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
    print(f'{key}:')
    print(value)
    print('-' * 50)
