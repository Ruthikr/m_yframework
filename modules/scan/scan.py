import subprocess

def run():
    ip=input("enter ip")
    res=subprocess.getoutput(f"nmap -p 80,443 {ip}")
    print(res)

