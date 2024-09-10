from utils import get_output_directory
import json
import subprocess
import os
def run(target):
    print(f"----Staring Recon-----")
    
    print("nmap scanning...")
    nmap(target)
    print("nmap scanning completed")

    print("nikto scanning...")
    nikto(target)
    print("nikto scanning completed")
   
    print("whois scanning...")
    whois(target)
    print("whois scanning completed")
    # Get the centralized output directory path
    
def nmap(target):
    nmap_res=subprocess.getoutput(f"nmap -p 80 {target}")
    print("NMAP RESULTS")
    print(nmap_res)
    output_path = os.path.join(get_output_directory(), f"nmap_results_{target}.json")
   # Save results to the JSON file in the output directory
    nmap_data = {"target": target, "result": nmap_res}
    with open(output_path, "w") as f:
        json.dump(nmap_data, f)

def nikto(target):
    nikto_res=subprocess.getoutput(f"nikto -h {target}")
    print("NIKTO RESULTS")
    print(nikto_res)
    output_path = os.path.join(get_output_directory(), f"nikto_results_{target}.json")
   # Save results to the JSON file in the output directory
    nikto_data = {"target": target, "result": nikto_res}
    with open(output_path, "w") as f:
        json.dump(nikto_data, f)

def whois(target):
    whois_res=subprocess.getoutput(f"whois {target}")
    print("WHOIS RESULTS")
    print(whois_res)
    output_path = os.path.join(get_output_directory(), f"whois_results_{target}.json")
   # Save results to the JSON file in the output directory                                                    with open(output_path, "w") as f:
    whois_data = {"target": target, "result": whois_res}
    with open(output_path,"w")as f:
        json.dump(whois_data,f)
