# IpSender

```service
[Unit]
Description=Send server IP to TG before load
After=multi-user.target

[Service]
User=dietpi
Group=dietpi
Type=simple
ExecStart={path to python} {path to script} 
[Install]
WantedBy=multi-user.target
```
