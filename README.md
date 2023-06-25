# IpSender

## Installation

1. Change to the project directory.
2. Install the required libraries with the command: `python3 -m pip install -r requirements.txt`
3. Create a file called `.env` and edit to add these lines:
```
USER_ID={your user id}
TOKEN='your token'
```
4. Create a systemd service with the configuration below

#### Systemd service config:
```
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
