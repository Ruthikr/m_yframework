import argparse
import logging
from colorama import Fore
from modules.recon.recon import nmap, nikto, whois, dig, whatweb, dnsrecon, run  # Import your recon tools
from utils.utils import load_config


def main():
    parser = argparse.ArgumentParser(description="Automated Recon Framework")
    parser.add_argument("--recon", help="Target for Reconnaissance", type=str)
    parser.add_argument("--config", help="Configuration file", type=str, default="config.json")
    args = parser.parse_args()

    config = load_config(args.config) if args.config else None

    if args.recon:
        target = args.recon
        tools = [nmap, nikto, whois, dig, whatweb, dnsrecon]  # List of imported functions
        
        # Ensure tools list is not empty before running scans
        if tools:
            run(target, tools)
        else:
            logging.error(Fore.RED + "No tools available to run.")
    elif config:
        for target in config.get("targets", []):
            tools = [globals()[tool] for tool in config.get("tools", []) if tool in globals()]
            
            # Ensure tools list is not empty before running scans
            if tools:
                run(target, tools)
            else:
                logging.error(Fore.RED + f"No tools specified for target {target}.")
    else:
        logging.error(Fore.RED + "No target or configuration file specified.")

if __name__ == "__main__":
    main()
