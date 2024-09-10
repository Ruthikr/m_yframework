import json
import subprocess
import os
import argparse
import logging
from colorama import init, Fore,Style
from concurrent.futures import ThreadPoolExecutor
from utils.utils import get_output_directory


# Initialize colorama for colored output
init(autoreset=True)

# Set up logging to log file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("framework.log"),
        logging.StreamHandler()
    ]
)

def run(target, tools):
    """Main function to run selected tools on the given target."""
    logging.info(Fore.CYAN + f"---- Starting Recon on {target} ----\n")

    with ThreadPoolExecutor(max_workers=len(tools)) as executor:
        futures = [executor.submit(tool, target) for tool in tools]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(Fore.RED + f"Error: {e}")

def nmap(target):
    """Run an Nmap scan and display the output in real-time."""
    logging.info(Fore.YELLOW + "Running Nmap scan...\n")
    try: 
        commands=["nmap","-p","80",target]
        nmap_res= subprocess.getoutput(f"nmap -p 80,443 -sV {target}")
        print(Fore.GREEN + "NMAP RESULTS")
        print(nmap_res)
        if "error" in nmap_res.lower():
            raise RuntimeError(f"Nmap encountered an error: {nmap_res}")

        save_results(target, nmap_res, "nmap_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running Nmap: {e}")

def nikto(target):
    """Run a Nikto scan and display the output in real-time."""
    logging.info(Fore.YELLOW + "Running Nikto scan...\n")
    try:
        nikto_res = subprocess.getoutput(f"nikto -h {target}")
        print(Fore.GREEN + "NIKTO RESULTS")
        print(nikto_res)

        if "error" in nikto_res.lower():
            raise RuntimeError(f"Nikto encountered an error: {nikto_res}")

        save_results(target, nikto_res, "nikto_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running Nikto: {e}")

def whois(target):
    """Run a WHOIS query and display the output."""
    logging.info(Fore.YELLOW + "Running WHOIS scan...\n")
    try:
        whois_res = subprocess.getoutput(f"whois {target}")
        print(Fore.GREEN + "WHOIS RESULTS")
        print(whois_res)

        if "error" in whois_res.lower():
            raise RuntimeError(f"WHOIS encountered an error: {whois_res}")

        save_results(target, whois_res, "whois_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running WHOIS: {e}")

def dig(target):
    """Run a DIG command to gather DNS information."""
    logging.info(Fore.YELLOW + "Running DIG scan...\n")
    try:
        dig_res = subprocess.getoutput(f"dig {target} ANY")
        print(Fore.GREEN + "DIG RESULTS")
        print(dig_res)

        save_results(target, dig_res, "dig_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running DIG: {e}")

def whatweb(target):
    """Run WhatWeb to detect website technology."""
    logging.info(Fore.YELLOW + "Running WhatWeb scan...\n")
    try:
        whatweb_res = subprocess.getoutput(f"whatweb {target}")
        print(Fore.GREEN + "WHATWEB RESULTS")
        print(whatweb_res)

        save_results(target, whatweb_res, "whatweb_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running WhatWeb: {e}")

def dnsrecon(target):
    """Run DNSRecon to gather DNS information."""
    logging.info(Fore.YELLOW + "Running DNSRecon scan...\n")
    try:
        dnsrecon_res = subprocess.getoutput(f"dnsrecon -d {target}")
        print(Fore.GREEN + "DNSRECON RESULTS")
        print(dnsrecon_res)

        save_results(target, dnsrecon_res, "dnsrecon_results")

    except Exception as e:
        logging.error(Fore.RED + f"Error running DNSRecon: {e}")

def save_results(target, results, scan_type):
    """Save the scan results to a JSON file in the target's output directory."""
    output_dir = os.path.join(get_output_directory(), target)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{scan_type}.json")

    try:
        with open(output_path, "w") as f:
            json.dump({"target": target, "result": results}, f)
        logging.info(Fore.CYAN + f"\n{scan_type.capitalize()} results saved to {output_path}\n")

    except IOError as e:
        logging.error(Fore.RED + f"Failed to save results: {e}")

def load_config(config_file):
    """Load configuration from a JSON file."""
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except (IOError, json.JSONDecodeError) as e:
        logging.error(Fore.RED + f"Error loading configuration file: {e}")
        return None


