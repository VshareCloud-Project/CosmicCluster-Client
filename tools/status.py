import os
import sys
import re
import subprocess

def get_cpu_info():
    """
    Get CPU information
    """
    cpuinfo = {}
    with open("/proc/cpuinfo") as f:
        for line in f:
            if line.strip():
                key, value = line.split(":", 1)
                cpuinfo[key.strip()] = value.strip()
    return cpuinfo

if __name__ == "__main__":
    print(get_cpu_info())

def get_cpu_cores_num():
    """
    Get CPU cores number
    """
    return os.cpu_count()

if __name__ == "__main__":
    print(get_cpu_cores_num())

def get_cpu_usage():
    """
    Get CPU usage
    """
    cpu_usage = os.popen("top -b -n 2 -d 0.01 | grep Cpu | tail -n 1").read().split(",")[0].split(":")[1].strip()
    return cpu_usage

if __name__ == "__main__":
    print(get_cpu_usage())

def get_mem_info():
    """
    Get memory information
    """
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            if line.strip():
                key, value = line.split(":", 1)
                meminfo[key.strip()] = value.strip()
    return meminfo

def get_mem_total()->int:
    """
    Get memory total
    """
    mem_total_str = get_mem_info()["MemTotal"]
    mem_total = int(mem_total_str.split(" ")[0])
    mem_code = mem_total_str.split(" ")[1]
    if mem_code.lower() == "kb":
        mem_total = mem_total * 1024
    elif mem_code.lower() == "mb":
        mem_total = mem_total * 1024 * 1024
    elif mem_code.lower() == "gb":
        mem_total = mem_total * 1024 * 1024 * 1024
    elif mem_code.lower() == "tb":
        mem_total = mem_total * 1024 * 1024 * 1024 * 1024
    return mem_total

if __name__ == "__main__":
    print(get_mem_total())

def get_mem_free():
    """
    Get memory free
    """
    mem_free_str = get_mem_info()["MemFree"]
    mem_free = int(mem_free_str.split(" ")[0])
    mem_code = mem_free_str.split(" ")[1]
    if mem_code.lower() == "kb":
        mem_free = mem_free * 1024
    elif mem_code.lower() == "mb":
        mem_free = mem_free * 1024 * 1024
    elif mem_code.lower() == "gb":
        mem_free = mem_free * 1024 * 1024 * 1024
    elif mem_code.lower() == "tb":
        mem_free = mem_free * 1024 * 1024 * 1024 * 1024
    return mem_free

if __name__ == "__main__":
    print(get_mem_free())

def get_disk_info():
    """
    Get disk information
    """
    disk_info = subprocess.getoutput("df").split("\n")
    disk_info = disk_info[1:]
    disk_info_detail = {}
    for i in range(len(disk_info)):
        disk_info_detail[re.split(r"[ ]+",disk_info[i])[5]] = {
            "filesystem": re.split(r"[ ]+",disk_info[i])[0],
            "size": re.split(r"[ ]+",disk_info[i])[1],
            "used": re.split(r"[ ]+",disk_info[i])[2],
            "available": re.split(r"[ ]+",disk_info[i])[3],
            "use": re.split(r"[ ]+",disk_info[i])[4][0:-1],
            "mounted_on": re.split(r"[ ]+",disk_info[i])[5]
        }
    return disk_info_detail

if __name__ == "__main__":
    print(get_disk_info())
