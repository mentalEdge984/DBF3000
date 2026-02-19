# DBF3000 - Directory Brute Forcer

**DBF3000** is a multi-threaded, intelligent web directory scanner written in Python. It features automatic calibration, smart filtering for wildcard redirects, and a professional CLI interface.

## Features
- 🚀 **Multi-Threaded:** Rips through wordlists with concurrent workers.
- 🧠 **Smart Calibration:** Detects "Catch-All" (Wildcard) redirects and auto-silences false positives.
- 🎯 **Sniper Mode:** Check single files/paths instantly bypassing the wordlist.
- 📝 **Auto-Logging:** Intelligently saves discoveries to `scan_<target>.txt`.

## Help Menu
```
usage: DBF3000.py [-h] [-u URL] [-l LIST] [-w WORKERS] [-v] [-f FIND] [-o OUTPUT]

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

# Interactive Mode (Prompts for target)
```./DBF3000.py
```
# Standard Scan
```
./DBF3000.py -u [https://example.com](https://example.com)
```
# Turbo Scan (100 workers, Custom Wordlist)
```
./DBF3000.py -u [https://example.com](https://example.com) -w 100 -l /path/to/wordlist.txt
```
# Sniper Mode (Check one specific file)
```
./DBF3000.py -u [https://example.com](https://example.com) -f admin/login.php
```
