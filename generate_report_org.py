import os
import json
from jinja2 import Template

def read_results(output_directory):
    results = {}
    for filename in os.listdir(output_directory):
        if filename.endswith(".json"):
            tool_name = filename.split('_results.json')[0]
            with open(os.path.join(output_directory, filename)) as f:
                results[tool_name] = json.load(f)
    return results

def generate_html_report(target, results):
    # Define the HTML template with Jinja2
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recon Results Report for {{ target }}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div class="container mt-4">
            <h1 class="text-center bg-primary text-white p-2">Recon Results Report for {{ target }}</h1>
            <canvas id="resultsChart" width="400" height="200"></canvas>
            <script>
                var ctx = document.getElementById('resultsChart').getContext('2d');
                var chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: {{ results.keys()|list }},
                        datasets: [{
                            label: 'Data Size of Tool Results',
                            data: {{ results.values()|map('length')|list }},
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            </script>
            {% for tool, result in results.items() %}
            <div class="card mt-3">
                <div class="card-header bg-info text-white" data-bs-toggle="collapse" data-bs-target="#collapse{{ loop.index }}">
                    {{ tool.capitalize() }} Results
                </div>
                <div id="collapse{{ loop.index }}" class="collapse">
                    <div class="card-body">
                        <pre>{{ result | tojson(indent=2) }}</pre>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    jinja_template = Template(template)
    html_content = jinja_template.render(target=target, results=results)

    report_path = os.path.join(output_directory, 'report', 'recon_report.html')
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w') as f:
        f.write(html_content)

    print(f"Report generated successfully at {report_path}")

if __name__ == "__main__":
    output_directory = "output/maxdataentryservices.com"  # Example directory
    results = read_results(output_directory)
    target_name = os.path.basename(output_directory)
    generate_html_report(target_name, results)
