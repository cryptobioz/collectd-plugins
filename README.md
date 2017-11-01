# Collectd plugins

Just some Collectd plugins mainly written in Python.

## How to use

### Out-of-memory

In `/etc/collectd/collectd.conf.d/out-of-memory.conf`:

```
LoadPlugin python
<Plugin python>
  ModulePath "/opt/collectd-plugins"
  Import "out-of-memory"
</Plugin>
```
