import subprocess
import threading
import os

def run_tool(command, output_file, tool_name):
    with open(output_file, 'w') as file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Starting {tool_name}...")
        for line in process.stdout:
            # Write the line to the output file
            file.write(line)
            # Print the line to the console
            print(f"[{tool_name}] {line}", end='')  # Use `end=''` to avoid adding extra new lines
        process.wait()
        print(f"{tool_name} finished.")

def run_tool_in_thread(command, output_dir, tool_name):
    output_file = os.path.join(output_dir, f"{tool_name}_scan.txt")
    thread = threading.Thread(target=run_tool, args=(command, output_file, tool_name))
    thread.start()
    return thread

# Example usage
def main():
    output_dir = "path/to/output"

    tools = [
        {"name": "nikto", "command": ["nikto", "-h", "example.com"], "file_suffix": "nikto"},
        {"name": "nmap", "command": ["nmap", "-A", "example.com"], "file_suffix": "nmap"},
        # Add more tools as needed
    ]

    threads = []
    for tool in tools:
        thread = run_tool_in_thread(tool["command"], output_dir, tool["name"])
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
