import os

def create_report(output_directory):
    # Load recon, analysis, and Vulners results
    recon_files = [f for f in os.listdir(output_directory) if f.endswith('.json')]
    report_data = {}

    for file in recon_files:
        with open(os.path.join(output_directory, file), 'r') as f:
            report_data[file] = f.read()

    # Create HTML content
    html_content = f"<html><head><title>Report for {output_directory}</title></head><body>"
    html_content += "<h1>Reconnaissance and Vulnerability Report</h1>"

    for tool, result in report_data.items():
        html_content += f"<h2>{tool}</h2><pre>{result}</pre>"

    html_content += "</body></html>"

    # Save the report
    report_path = os.path.join(output_directory, 'final_report.html')
    with open(report_path, 'w') as f:
        f.write(html_content)

    print(f"Report generated successfully at {report_path}")
