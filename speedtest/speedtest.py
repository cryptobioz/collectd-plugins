# coding: utf8

import collectd
import os
import subprocess
import json

INTERVAL = 10
SERVERS = []
SPEEDTEST_BIN = None

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def run_speedtest(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = p.stdout.readlines()
    result = json.loads(output[0])
    stat = collectd.Values(type="gauge", type_instance="ping")
    stat.plugin = "speedtest"
    stat.plugin_instance = result['server']['host'].split(":", 1)[0]
    stat.dispatch(values=[1])
    stat.dispatch(values=[float(result['ping'])], interval=INTERVAL)
    stat = collectd.Values(type="gauge", type_instance="download")
    stat.plugin = "speedtest"
    stat.plugin_instance = result['server']['host'].split(":", 1)[0]
    stat.dispatch(values=[float(result['download']) / 1000.0 / 1000.0], interval=INTERVAL)
    stat = collectd.Values(type="gauge", type_instance="upload")
    stat.plugin = "speedtest"
    stat.plugin_instance = result['server']['host'].split(":", 1)[0]
    stat.dispatch(values=[float(result['upload']) / 1000.0 / 1000.0], interval=INTERVAL)

def config_func(config):

    # Checking for speedtest-cli binary
    s = which("speedtest-cli")
    if s is None:
        collectd.error('speedtest plugin: speedtest-cli not found.')
    else:
        global SPEEDTEST_BIN
        SPEEDTEST_BIN = s

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'interval':
            global INTERVAL
            INTERVAL = int(val)

        if key == 'serverid':
            global SERVERS
            SERVERS.append(int(val))
    if len(SERVERS) == 0:
        collectd.info('speedtest plugin: No server specified, speedtest-cli will use the best server.')
    
    collectd.register_read(read_func, INTERVAL)

def read_func():
    if len(SERVERS) == 0:
        command = "%s --json" % SPEEDTEST_BIN
        run_speedtest(command)

    else:
        for server in SERVERS:
            command = "%s --server %d --json" % (SPEEDTEST_BIN, server)
            run_speedtest(command)

collectd.register_config(config_func)
