import sys
import platform
import subprocess
from prettytable import PrettyTable

def run_command(command):
         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
         output, _ = process.communicate()
         return output.decode('utf-8').strip()
         
         def bytes_to_gb(bytes_value):
                  gb = bytes_value / (1024 ** 3)
                  return f"{gb:.2f} GB"
                  
         def get_host_name():
                  return run_command('scutil --get ComputerName')
         
         def get_os_info():
                  os_name = platform.system()
                  os_version = platform.mac_ver()[0]
                  return os_name, os_version
         
         def get_processor_info():
                  return run_command('sysctl -n machdep.cpu.brand_string')
                  
         def get_memory_info():
                  memory_info_bytes = int(run_command('sysctl -n hw.memsize'))
                  return bytes_to_gb(memory_info_bytes)
         def get_disk_info():
                  disk_info = run_command('df -H | grep /dev/disk1')
                  return disk_info

         def get_network_interfaces():
                  network_interfaces = run_command('ifconfig | grep "inet " | awk \'{print $2}\'')
                  return network_interfaces
                  
                  host_name = get_host_name()
                  os_name, os_version = get_os_info()
                  processor_name = get_processor_info()
                  memory_info = get_memory_info()
                  disk_info = get_disk_info()
                  network_interfaces = get_network_interfaces()

                  table = PrettyTable()
                  table.field_names = ["Category", "Information"]
                  table.add_row(["Host Name", host_name])
                  table.add_row(["OS Name", os_name])
                  table.add_row(["OS Version", os_version])
                  table.add_row(["Processor", processor_name])
                  table.add_row(["Memory", memory_info])
                  table.add_row(["Disk Information", disk_info])
                  table.add_row(["Network Interfaces", network_interfaces])

                  sys.stdout.write(table.get_string())
   
