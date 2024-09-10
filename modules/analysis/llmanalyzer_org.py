from colorama import init,Fore,Style
import os
from vulners import Vulners
# Ensure you have the OpenAI library installed
from utils.utils import get_output_directory
import langchain
from langchain_ollama.llms import OllamaLLM

init(autoreset=True)

def analyze_results(output_directory):
    # Load all recon data from the output directory
    recon_files = [f for f in os.listdir(output_directory) if f.endswith('.json')]
    recon_data = {}

    for file in recon_files:
        with open(os.path.join(output_directory, file), 'r') as f:
            recon_data[file] = f.read()

    # Use OpenAI's LLM to analyze the recon data
    model=OllamaLLM(model="gemma2:2b")
    prompt=f"Analyze the following reconnaissance data and suggest potential vulnerabilities t o query the vulners api:\n{recon_data}",
    response=model.invoke(prompt)
    print(Style.BRIGHT + Fore.RED + "LLM RESULTS")
    print(response)
    # Extract useful information and queries from LLM output
    analysis_output = response
    # Perform search using Vulners API
    vulners_api = Vulners(api_key="82YCI0CG6C68F9VSXS8W2YT2RFRHVUW4X3YJHDXCQ8RK223M8ZA2OT72FNM71QH0")
    results = vulners_api.search(analysis_output)

    # Save the analysis output to a file
    with open(os.path.join(output_directory, 'analysis_results.json'), 'w') as f:
        f.write(results)

    return results
