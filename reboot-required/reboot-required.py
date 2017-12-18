import collectd
import os

def config_func(config):
    pass

def read_func():
    required = 0
    if os.path.isfile("/var/run/reboot-required"):
        required = 1

    stat = collectd.Values(type="gauge")
    stat.plugin = "reboot-required"
    stat.dispatch(values=[required])

collectd.register_config(config_func)
collectd.register_read(read_func)
