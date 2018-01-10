import collectd
import subprocess
import re

def config_func(config):
    pass

def read_func():
    kpti_enabled = 0

    # Looking for flags in /proc/cpuinfo
    f = open("/proc/cpuinfo", "r")
    for line in f:
        if re.search("^flags", line):
            if re.search("pti", line):
                kpti_enabled = 1
            elif re.search("kaiser", line):
                kpti_enabled = 1
    f.close()

    # Looking for flags into the dmesg output
    p = subprocess.Popen("dmesg | grep -Eq 'Kernel/User page tables isolation: enabled|Kernel page table isolation enabled'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if p.stdout.readlines() != []:
        kpti_enabled = 1

    stat = collectd.Values(type="gauge")
    stat.plugin = "kpti"
    stat.dispatch(values=[kpti_enabled])

collectd.register_config(config_func)
collectd.register_read(read_func)
