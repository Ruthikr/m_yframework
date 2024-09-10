from langchain import OpenAI
from langchain.chains import LLMChain
from utils import utils
import vulners

# Initialize Vulners API client
vulners_api = vulners.Vulners(api_key='82YCI0CG6C68F9VSXS8W2YT2RFRHVUW4X3YJHDXCQ8RK223M8ZA2OT72FNM71QH0')

def analyze_with_llm():
    # Initialize LLM
    llm = OpenAI(temperature=0.5)
    llm_chain = LLMChain(prompt="Analyze the recon results to find vulnerabilities.")

    output_dir = utils.get_output_directory()
    targets = os.listdir(output_dir)
    
    for target in targets:
        print(f"Analyzing results for target: {target}")
        results = utils.read_results(target)
        
        for tool, data in results.items():
            analysis_input = f"Tool: {tool}\nResults: {data}\n"
            vuln_query = llm_chain.run(analysis_input)

            # Fetch data from Vulners API based on query
            vulns = vulners_api.search(vuln_query)
            print(f"Potential vulnerabilities for {target}:\n{vulns}")
