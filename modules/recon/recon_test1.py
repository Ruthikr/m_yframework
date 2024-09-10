import json
import subprocess
import os
from colorama import init, Fore
from utils import get_output_directory

# Initialize colorama
init(autoreset=True)

def run(target):
    print(Fore.CYAN + "---- Starting Recon -----\n")

    # Run scans and display results in real-time
    nmap(target)
    nikto(target)
    whois(target)

def nmap(target):
    """Run an Nmap scan and display the output in real-time."""
    print(Fore.YELLOW + "Running Nmap scan...\n")
    try:
        # Use subprocess.Popen to get real-time output
        process = subprocess.Popen(
            ["nmap", "-p", "80", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Display output line by line
        nmap_res = ""
        for line in process.stdout:
            print(line, end="")
            nmap_res += line

        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args)

        # Save results to the output directory
        save_results(target, nmap_res, "nmap_results")

    except Exception as e:
        print(Fore.RED + f"Error running Nmap: {e}")

def nikto(target):
    """Run a Nikto scan and display the output in real-time."""
    print(Fore.YELLOW + "Running Nikto scan...\n")
    try:
        nikto_res = subprocess.getoutput(f"nikto -h {target}")
        print(Fore.GREEN + "NIKTO RESULTS")
        print(nikto_res)

        if "error" in nikto_res.lower():
            raise RuntimeError(f"Nikto encountered an error: {nikto_res}")

        # Save results to the output directory
        save_results(target, nikto_res, "nikto_results")

    except Exception as e:
        print(Fore.RED + f"Error running Nikto: {e}")

def whois(target):
    """Run a WHOIS query and display the output."""
    print(Fore.YELLOW + "Running WHOIS scan...\n")
    try:
        whois_res = subprocess.getoutput(f"whois {target}")
        print(Fore.GREEN + "WHOIS RESULTS")
        print(whois_res)

        if "error" in whois_res.lower():
            raise RuntimeError(f"WHOIS encountered an error: {whois_res}")

        # Save results to the output directory
        save_results(target, whois_res, "whois_results")

    except Exception as e:
        print(Fore.RED + f"Error running WHOIS: {e}")

def save_results(target, results, scan_type):
    """Save the scan results to a JSON file in the target's output directory."""
    # Create a directory for the specific target
    output_dir = os.path.join(get_output_directory(), target)
    os.makedirs(output_dir, exist_ok=True)

    # Define the path to save results
    output_path = os.path.join(output_dir, f"{scan_type}.json")

    try:
        with open(output_path, "w") as f:
            json.dump({"target": target, "result": results}, f)
        print(Fore.CYAN + f"\n{scan_type.capitalize()} results saved to {output_path}\n")

    except IOError as e:
        print(Fore.RED + f"Failed to save results: {e}")


