# DBF3000 - Directory Brute Forcer

**DBF3000** is a multi-threaded, intelligent web directory scanner written entirely in Python. It features automatic calibration, smart filtering for wildcard redirects, and a professional CLI interface.

## Features
- 🚀 **Multi-Threaded:** Rips through wordlists with concurrent workers.
- 🧠 **Smart Calibration:** Detects "Catch-All" (Wildcard) redirects and auto-silences false positives.
- 🎯 **Sniper Mode:** Check single files/paths instantly bypassing the wordlist.
- 📝 **Auto-Logging:** Intelligently saves discoveries to `scan_<target>.txt`.

# Installation

## Using Kali/ParrotOS

# Download the repository
```
git clone [https://github.com/mentalEdge984/DBF3000.git](https://github.com/mentalEdge984/DBF3000.git)
cd DBF3000
```

# Make the script executable
```
chmod +x DBF3000.py
```

# Install it globally as a system command(removes the need to prefix with python3 and also removes the '.py')
```
sudo mv DBF3000.py /usr/local/bin/DBF3000
```

## Installation with Windows 10/11

# Open command prompt(cmd) as administrator
- go to the start menu and type cmd
- right click command prompt(little black box icon)
- left click 'run as administrator'
- confirm

# Download the repository
```
git clone [https://github.com/mentalEdge984/DBF3000.git](https://github.com/mentalEdge984/DBF3000.git)
cd DBF3000
```

# Run the script
```
python DBF3000.py
```

## Help Menu

usage: DBF3000 [-h] [-u URL] [-l LIST] [-w WORKERS] [-v] [-f FIND] [-o OUTPUT]

DBF3000: The Directory Brute Forcer (Pro Edition)

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Target URL
  -l LIST, --list LIST  Wordlist path (Default: /usr/share/wordlists/dirb/common.txt)
  -w WORKERS, --workers WORKERS
                        Number of workers (Default: 50)
  -v, --verbose         Verbose mode
  -f FIND, --find FIND  Specific path to check (Sniper Mode)
  -o OUTPUT, --output OUTPUT
                        Output file (Default: scan_<domain>.txt)

## Usage

# Interactive mode - prompts for target website (after following the above guide to make it fully executable, otherwise use python3 DBF3000.py)
```
DBF3000
```

# Standard Scan (default 50 workers)
```
DBF3000 -u https://[site_name_here]
```

# Turbo Scan (increased workers, custom wordlist)
```
DBF3000 -u https://[site_name_here] -l /path/to/your/wordlist -w 150
```

# Sniper Scan (specify the filename/folder)
```
DBF3000 -u [https://[site_name_here] -f admin/login.php
```

## ⚠️ DANGER & DISCLAIMER

**DBF3000 is an aggressive, high-concurrency reconnaissance tool.** This software is provided for **educational purposes and authorized, contracted security testing only**. 

**🔥 NETWORK WARNING:** Running this tool with a high worker count (`-w 300+`) can and will cause Denial of Service (DoS) conditions on standard home and small-business routers by exhausting the NAT state table. It may also trigger upstream ISP rate-limiting.

**Do not point this at infrastructure you do not own or do not have explicit, written permission to test.** The developer assumes no liability and is not responsible for any network crashes, hardware lockups, or legal issues caused by the misuse of this program.
