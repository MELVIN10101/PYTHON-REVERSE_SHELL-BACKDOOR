# Reverse Shell using Python

## Overview
This project is a Python-based reverse shell that allows remote access to a compromised system. It consists of two scripts:
- `backdoor.py`: Runs on the target machine, connects back to the attacker's machine, and allows remote execution of commands.
- `host.py`: Runs on the attacker's machine, listens for incoming connections, and enables interaction with compromised machines.

## Features
- Remote command execution
- Detects sandbox/virtual environments
- Takes screenshots of the victim's screen
- Opens websites remotely
- Locks the victim's machine

## Installation & Usage

### Attacker Machine (host.py)
1. Modify `strHost` in `host.py` to your local IP address.
2. Run the script:
   ```bash
   python host.py
   ```
3. Wait for incoming connections.

### Target Machine (backdoor.py)
1. Modify `strHost` in `backdoor.py` to the attacker's IP.
2. Run the script:
   ```bash
   python backdoor.py
   ```
3. The script will attempt to connect back to the attacker's machine.

## Commands
Once a connection is established, the following commands can be executed:
- `cmd` - Opens an interactive shell
- `msg <message>` - Displays a message box
- `site <URL>` - Opens a website in the victim’s browser
- `screen` - Takes a screenshot of the victim’s screen
- `lock` - Locks the victim’s machine
- `exit` - Terminates the connection

## Disclaimer
**This tool is for educational and ethical penetration testing purposes only. Unauthorized use of this script is illegal and may result in severe consequences. The author is not responsible for any misuse.**

