# Collectd plugins

## How to use

### Out-of-memory

In `/etc/collectd/collectd.conf.d/out-of-memory.conf`, write:

```
LoadPlugin python
<Plugin python>
  ModulePath "/opt/collectd-plugins"
  Import "out-of-memory"
</Plugin>
```

### Speedtest

*Note: To use it, you must have the [speedtest-cli](https://github.com/sivel/speedtest-cli) tool installed.* 

In `/etc/collectd/collectd.conf.d/speedtest.conf`, write:

```
LoadPlugin python
<Plugin python>
  ModulePath "/opt/collectd-plugins"
  Import "speedtest"
  <Module speedtest>
    Interval 300
    ServerID 10240
    ServerID 8782
  </Module>
</Plugin>
```

You should provide an important *Interval* because the speedtest may take a while.

You can set as *ServerID* as you want. If you do not provide this parameter, speedtest-cli will automatically use the best server.

On reports, the *plugin_instance* is the remote host and the *type_instance* could be "ping", "download" or "upload".

### Reboot required

Returns 1 if a reboot is required.

In `/etc/collectd/collectd.conf.d/reboot-required.conf`, write:

```
LoadPlugin python
<Plugin python>
  ModulePath "/opt/collectd-plugins"
  Import "reboot-required"
</Plugin>
```
