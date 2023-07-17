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

    '''disk_info = run_command('diskutil list')
        disk_list_output = disk_info.split('\n')
    
        # Find the lines containing disk information
        disk_lines = [line for line in disk_list_output if 'Apple_APFS' in line or 'FAT32' in line]
    
        # Extract disk details and space information
        disk_details = []
        for line in disk_lines:
            line_parts = line.split()
            if len(line_parts) >= 9:
                disk_name = line_parts[5]
                space_used = line_parts[7]
                space_left = line_parts[8]
                disk_details.append(f"Disk {disk_name}: Space Used: {space_used}, Space Left: {space_left}")
    
        system_info['Disk Information'] = '\n'.join(disk_details)'''


    # Get network interfaces
    network_interfaces = run_command('ifconfig -a')
    ip_addresses_output = run_command('ifconfig | grep "inet " | awk \'{print $2}\'')
    ip_addresses = ip_addresses_output.split('\n')
    system_info['IP Addresses'] = ip_addresses
    network_cards_output = run_command('networksetup -listallhardwareports')
    network_cards = network_cards_output.split('\n')
    formatted_network_cards = '\n'.join(network_cards)
    system_info['Network Cards'] = formatted_network_cards

    
    #network_cards_output = run_command('networksetup -listallhardwareports')
    #network_cards = network_cards_output.split('\n')
    #system_info['Network Cards'] = network_cards
    
    
    
     # Get memory information
    total_memory_output = run_command('sysctl -n hw.memsize')
    total_memory = int(total_memory_output)
    total_memory_gb = total_memory / (1024**3)
    system_info['Total Memory'] = f"{total_memory_gb:.2f} GB"
    
    available_memory_output = run_command('vm_stat | grep "Pages free" | awk \'{print $3}\'')
    available_memory_pages = int(available_memory_output)
    available_memory_bytes = available_memory_pages * 4096
    available_memory_gb = available_memory_bytes / (1024**3)
    system_info['Available Memory'] = f"{available_memory_gb:.2f} GB"
    

    
    return system_info

# Get and print system information
system_info = get_system_info()
for key, value in system_info.items():
    print(f'{key}:')
    print(value)
    print('-' * 50)
