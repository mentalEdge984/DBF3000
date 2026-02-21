#!/usr/bin/env python3
import requests
from requests.adapters import HTTPAdapter
import sys
import concurrent.futures
import random
import string
import argparse
import os

# --- GLOBAL SETTINGS ---
IGNORE_REDIRECTS = False
LOG_FILE = ""
VERBOSE_MODE = False

# Create a global session object for Connection Pooling
session = requests.Session()

# --- 1. THE LOGGER ---
def save_log(message):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"[!] Error writing to log: {e}")

# --- 2. THE CALIBRATION CHECK ---
def run_calibration(target_url):
    global IGNORE_REDIRECTS
    
    if VERBOSE_MODE:
        print("[*] Verbose Mode ON: Skipping Smart Filter. All redirects will be shown.")
        return

    garbage = ''.join(random.choices(string.ascii_lowercase, k=8))
    calibration_url = f"{target_url}/{garbage}"
    
    print(f"[*] Calibrating with nonsense URL: {calibration_url} ...")
    
    try:
        r = session.get(calibration_url, timeout=5, allow_redirects=False)
        
        if r.status_code == 301 or r.status_code == 302:
            print(f"[!] ALERT: Site redirects invalid pages (Got {r.status_code}).")
            print("[!] Enabling SMART FILTER: Redirects will be hidden.")
            IGNORE_REDIRECTS = True
        elif r.status_code == 200:
            print(f"[!] WARNING: Site returns '200 OK' for everything. Expect False Positives.")
        else:
            print(f"[*] Calibration Passed: Invalid pages return {r.status_code}. Normal scan mode.")
            
    except requests.exceptions.RequestException:
        print("[!] Calibration Failed: Could not connect to site (is it down?).")
        sys.exit()

# --- 3. THE WORKER ---
def check_url(full_url):
    try:
        # Using the globally pooled session instead of a raw requests.get()
        response = session.get(full_url, timeout=3, allow_redirects=False)

        msg = None
        
        if response.status_code == 200:
            msg = f"[+] DISCOVERED: {full_url}"
        elif response.status_code == 403:
            msg = f"[-] LOCKED: {full_url} (Admin Only?)"
        elif response.status_code in [301, 302]:
            if VERBOSE_MODE or not IGNORE_REDIRECTS:
                msg = f"[*] REDIRECT: {full_url}"

        if msg:
            print(msg)
            save_log(msg)

    except requests.exceptions.RequestException:
        pass

# --- 4. THE COMMANDER ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBF3000: The Directory Brute Forcer (Pro Edition)")
    
    # Flags
    parser.add_argument("-u", "--url", help="Target URL")
    parser.add_argument("-l", "--list", default="/usr/share/wordlists/dirb/common.txt", help="Wordlist path")
    parser.add_argument("-w", "--workers", type=int, default=50, help="Number of workers")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("-f", "--find", help="Specific path to check (Sniper Mode)")
    parser.add_argument("-o", "--output", help="Output file or full path (Default: Auto-saves to Desktop)")

    args = parser.parse_args()

    # --- THE COOL LOGO ---
    RED = "\033[91m"
    RESET = "\033[0m"

    logo = f"""{RED}
    ██████╗ ██████╗ ███████╗██████╗  ██████╗  ██████╗  ██████╗ 
    ██╔══██╗██╔══██╗██╔════╝╚════██╗██╔═████╗██╔═████╗██╔═████╗
    ██║  ██║██████╔╝█████╗   █████╔╝██║██╔██║██║██╔██║██║██╔██║
    ██║  ██║██╔══██╗██╔══╝   ╚═══██╗████╔╝██║████╔╝██║████╔╝██║
    ██████╔╝██████╔╝██║     ██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝
    ╚═════╝ ╚═════╝ ╚═╝     ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ 
                                                  -- SCANNER --{RESET}
    """
    print(logo)

    # --- DANGER ZONE CHECK (>300 WORKERS) ---
    if args.workers > 300:
        print(f"\n{RED}[!!!] DANGER: EXTREME CONCURRENCY DETECTED ({args.workers} WORKERS) [!!!]{RESET}")
        print(f"{RED}[!] Running more than 300 workers will likely crash standard home routers{RESET}")
        print(f"{RED}[!] and cause a local Denial of Service (DoS).{RESET}")
        
        if hasattr(os, 'geteuid'):
            if os.geteuid() != 0:
                print(f"{RED}[!] WARNING: You are NOT running as root. High thread counts{RESET}")
                print(f"{RED}[!] may exhaust standard user socket limits and crash the script.{RESET}")
            else:
                print(f"[*] Root privileges confirmed. Socket limits optimized.")

        try:
            confirm = input(f"\n[*] Are you absolutely sure you want to proceed? (y/N): ").strip().lower()
            if confirm != 'y':
                print("[-] Scan aborted to protect network infrastructure.")
                sys.exit()
        except KeyboardInterrupt:
            print("\n[-] Scan aborted.")
            sys.exit()

    # --- CONFIGURE CONNECTION POOLING ---
    adapter = HTTPAdapter(pool_connections=args.workers, pool_maxsize=args.workers)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({'User-Agent': 'DBF3000-Scanner/1.1'})

    # --- FALLBACK LOGIC ---
    if not args.url:
        try:
            target_input = input(f"[*] Enter Target URL (e.g. https://demo.testfire.net): ").strip()
            if not target_input:
                print("[!] Error: No target provided. Exiting.")
                sys.exit()
            base_url = target_input.rstrip('/')
        except KeyboardInterrupt:
            print("\n[!] Exiting.")
            sys.exit()
    else:
        base_url = args.url.rstrip('/')

    # --- SMART AUTO-NAMING & ROUTING ---
    home_dir = os.path.expanduser('~')
    desktop_path = os.path.join(home_dir, 'Desktop')

    if args.output:
        # Check if they provided just a filename, or a specific path
        if os.path.dirname(args.output) == "":
            # Only a filename was given (e.g. "results.txt") -> Send to Desktop
            if os.path.exists(desktop_path):
                LOG_FILE = os.path.join(desktop_path, args.output)
            else:
                LOG_FILE = args.output
        else:
            # A specific path was given (e.g. "/tmp/results.txt") -> Respect it
            LOG_FILE = args.output
    else:
        # No flag was used -> Auto-generate name and send to Desktop
        clean_name = base_url.replace("http://", "").replace("https://", "").split('/')[0]
        clean_name = clean_name.replace(":", "_")
        auto_name = f"scan_{clean_name}.txt"
        
        if os.path.exists(desktop_path):
            LOG_FILE = os.path.join(desktop_path, auto_name)
        else:
            LOG_FILE = auto_name

    VERBOSE_MODE = args.verbose

    print(f"[*] Target:   {base_url}")
    print(f"[*] Output:   {LOG_FILE}")
    print(f"[*] Sessions: Keep-Alive Connection Pool Enabled ({args.workers} pipes)")
    
    # Init Log
    with open(LOG_FILE, "w") as f:
        f.write(f"--- Scan Results for {base_url} ---\n")

    # 1. Calibration
    run_calibration(base_url)
    
    # 2. TARGET SELECTION
    urls_to_scan = []
    
    if args.find:
        # SNIPER MODE
        specific_path = args.find.lstrip('/')
        print(f"[*] MODE: Sniper (Checking specific path only)")
        urls_to_scan.append(f"{base_url}/{specific_path}")
    else:
        # ARMY MODE
        try:
            print(f"[*] MODE: Army (Brute Force with Wordlist)")
            print(f"[*] Wordlist: {args.list}")
            
            with open(args.list, "r", encoding="utf-8", errors="ignore") as f:
                urls_to_scan = [f"{base_url}/{line.strip()}" for line in f if line.strip()]
            
            print(f"[*] Loaded {len(urls_to_scan)} paths.")
        except FileNotFoundError:
            print(f"[X] ERROR: Wordlist not found at {args.list}")
