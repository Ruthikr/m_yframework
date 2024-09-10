from colorama import init, Fore, Style
import os
from vulners import VulnersApi  # Use VulnersApi instead of Vulners
from utils.utils import get_output_directory
from langchain_ollama.llms import OllamaLLM

init(autoreset=True)

def analyze_results(output_directory):
    # Load all recon data from the output directory
    recon_files = [f for f in os.listdir(output_directory) if f.endswith('.json')]
    recon_data = {}

    for file in recon_files:
        with open(os.path.join(output_directory, file), 'r') as f:
            recon_data[file] = f.read()

    # Concatenate all recon data for LLM input
    recon_text = "\n".join(recon_data.values())

    # Use the refined prompt template for the LLM
    prompt = (
        "Analyze the following reconnaissance data and generate a concise list of "
        "keywords or phrases that are directly related to potential vulnerabilities "
        "or exploits. Provide only the keywords or phrases that would be relevant for "
        "a vulnerability search, without any additional explanations:\n\n"
        f"{recon_text}"
    )

    # Invoke the LLM with the refined prompt
    model = OllamaLLM(model="gemma2:2b")
    response = model.invoke(prompt)

    print(Style.BRIGHT + Fore.RED + "LLM RESULTS")
    print(response)

    # Extract useful information and queries from LLM output
    analysis_output = response.strip()  # Ensure output is clean for the API

    # Initialize VulnersApi client
    vulners_api = VulnersApi(api_key="82YCI0CG6C68F9VSXS8W2YT2RFRHVUW4X3YJHDXCQ8RK223M8ZA2OT72FNM71QH0")

    # Perform search using VulnersApi's find_all method
    results = vulners_api.find_all(analysis_output)

    # Convert ResultSet to string before saving to a file
    results_str = "\n".join(str(result) for result in results)

    # Save the analysis output to a file
    with open(os.path.join(output_directory, 'analysis_results.json'), 'w') as f:
        f.write(results_str)

    return results
