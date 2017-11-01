import collectd
import subprocess
import re

def config_func(config):
    pass

def read_func():
    programs = []
    command = "dmesg | grep 'Out of memory: Kill process'"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()
    for line in output:
        m = re.search(r"\((.*)\) score", line)
        if m:
            programs.append(m.groups()[0])
    data = {x:programs.count(x) for x in programs}
    for key, value in data.iteritems():
        stat = collectd.Values(type="gauge")
        stat.plugin = "oom"
        stat.plugin_instance = key 
        stat.dispatch(values=[value])

collectd.register_config(config_func)
collectd.register_read(read_func)
