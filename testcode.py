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
    # disk_info = run_command('diskutil list')
    # system_info['Disk Information'] = disk_info

    # Get disk information
disk_list_output = run_command('diskutil list')
disk_list_lines = disk_list_output.split('\n')

# Find the disk with the highest usage
highest_usage_disk = None
highest_usage_value = -1

for line in disk_list_lines:
    if 'Apple_APFS' in line:
        line_parts = line.split()
        if len(line_parts) > 3:
            usage_percentage = line_parts[-2].replace('%', '')
            try:
                usage_value = int(usage_percentage)
                if usage_value > highest_usage_value:
                    highest_usage_value = usage_value
                    highest_usage_disk = line_parts[0]
            except ValueError:
                continue

# Get space usage information for the highest usage disk
if highest_usage_disk:
    disk_usage_output = run_command(f'df -H {highest_usage_disk}')
    disk_usage_lines = disk_usage_output.split('\n')
    if len(disk_usage_lines) > 1:
        space_used_line = disk_usage_lines[1]
        space_used_parts = space_used_line.split()
        if len(space_used_parts) > 4:
            space_used = space_used_parts[2]
            print(f"Disk Information: Disk {highest_usage_disk}, Space Used: {space_used}")
    
    # Get network interfaces
    network_interfaces = run_command('ifconfig -a')
    system_info['Network Interfaces'] = network_interfaces
    
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





