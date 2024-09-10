import argparse
import os
from modules.recon import recon
from utils.utils import get_output_directory
from modules.analysis import llmanalyzer
from modules.reporting import generate_report
from modules.recon.recon import nmap,dig,dnsrecon,whatweb,nikto,whois 
def main():
    parser = argparse.ArgumentParser(description="Bug Bounty Framework")
    parser.add_argument("--target",type=str, help="Target domain or IP for reconnaissance")
    args = parser.parse_args()

    target = args.target
    output_directory = os.path.join(get_output_directory(), target)

    tools=[nmap,dnsrecon,whois,whatweb,nikto]
    # Step 1: Run Reconnaissance
    recon.run(target,tools)

    # Step 2: Analyze Recon Results with LLM
    llmanalyzer.analyze_results(output_directory)

    # Step 3: Generate Final Report
    generate_report.create_report(output_directory)

if __name__ == "__main__":
    main()
