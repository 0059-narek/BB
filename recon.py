import os
import subprocess
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup

# color
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
C = "\033[0m"

# 0059 RECON banner 
def show_banner():
    os.system('clear')
    banner = f"""{B}
  ██████   ██████  ███████  █████      ██████  ███████  ██████  ██████  ███    ██ 
 ███  ███ ███  ███ ██      ██   ██     ██   ██ ██      ██      ██    ██ ████   ██ 
 ███  ███ ███  ███ ███████  ██████     ██████  █████   ██      ██    ██ ██ ██  ██ 
 ███  ███ ███  ███      ██      ██     ██   ██ ██      ██      ██    ██ ██  ██ ██ 
  ██████   ██████  ███████      ██     ██   ██ ███████  ██████  ██████  ██   ████ 
                                                                                  
                          {Y}v1.2 - Created by Narek0059{C}
    """
    print(banner)

show_banner()

total_start = time.time()

# filter
def run_silent(command, description):
    print(f"{Y}[*] {description}...{C}", end="\r")
    start = time.time()
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end = time.time()

    duration = end - start
    print(f"{G}[+] {description} DONE! ({round(duration, 2)}s){C}")
    return duration

# flag
parse = argparse.ArgumentParser(description="0059 RECON")
# -d target
parse.add_argument("-d", "--domain", help="Target Domain Name", required=True)
# -t threads
parse.add_argument("-t", "--threads", default=10, type=int, help="Set speed default=10")
# -H header
parse.add_argument("-H", "--header", help="Add custom header (e.g. -H 'Auth: keys')")
# -n nuclei
parse.add_argument("-n", "--nuclei", help="for using nuclei tool", action="store_true")
# -s subzy
parse.add_argument("-s", "--subzy", help="for using subzy tool", action="store_true")

# parse
args = parse.parse_args()

target = args.domain

# file
subfinder = "subfinder.txt"
sublist3r = "sublist3r.txt"

# file subfinder
if os.path.exists(subfinder):
	pat = input(f"File subfinder.txt already exists. Use it? (y/n): ")
	if pat.lower() == "y":
		print("Continuing with existing file.")
	else:
		subfinder = input("Enter a new filename for results (e.g., custom.txt): ")
		print(f"Continuing recon with file:")

# subfinder
subfinderr = f"subfinder -d {target} -all -recursive -o {subfinder}"
run_silent(subfinderr, "Running Subfinder enumeration")

# file sublist3r
if os.path.exists(sublist3r):
	pat = input(f"{sublist3r} File already exists. Continue using it? (y/n): ")
	if pat.lower() == "y":
		print("Continuing...")
	else:
		sublist3r = input("Enter filename in .txt format: ")

# sublist3r
sublist3rr = f"sublist3r -d {target} -o {sublist3r}"
run_silent(sublist3rr, "Running Sublist3r enumeration")

# synapsint
print(f"{Y}[*] Running Synapsint enumeration...{C}", end="\r")
syn_start = time.time()

try:
    synapsint_url = "https://synapsint.com/report.php"
    payload = {"search": target, "btnradio": "1"}
    response = requests.post(synapsint_url, data=payload, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all("a", class_="text-decoration-none text-secondary")

    with open('synapsint.txt', 'w') as f:
        for link in result:
            href = link.get('href')
            if href and target in href:
                f.write(href + "\n")
    
    syn_end = time.time()
    print(f"{G}[+] Running Synapsint enumeration DONE! ({round(syn_end - syn_start, 2)}s){C}")
except Exception as e:
    print(f"{Y}[!] Synapsint error: {e}{C}")

script_end = time.time()
total_duration = script_end - total_start

print(f"\n{G}[!] Recon complete! Total time: {round(total_duration, 2)}s{C}")
print(f"[!] Results are sorted. Run 'ls' to see the files.")

# sort
sort = f"cat {subfinder} synapsint.txt {sublist3r} | sort -u > sort.txt"
run_silent(sort, "Merging and sorting subdomains")

# del
os.remove(subfinder)
os.remove(sublist3r)
#os.remove('synapsint.txt')

# httpx 
httpx = f"cat sort.txt | httpx -sc -title -td -t 20 -o live.txt"
run_silent(httpx, "Checking live domains with HTTPX")

# sort
cat200 = f"""cat live.txt | grep "20" | cut -d ' ' -f1 > 2xx.txt"""
cat300 = f"""cat live.txt | grep "30" | cut -d ' ' -f1 > 3xx.txt"""
cat400 = f"""cat live.txt | grep "40" | cut -d ' ' -f1 > 4xx.txt"""
cat500 = f"""cat live.txt | grep "50" | cut -d ' ' -f1 > 5xx.txt"""

run_silent(cat200, "Filtering 2xx status codes")
run_silent(cat300, "Filtering 3xx status codes")
run_silent(cat400, "Filtering 4xx status codes")
run_silent(cat500, "Filtering 5xx status codes")

# Nuclei
if args.nuclei:
    if os.path.exists("2xx.txt") and os.path.getsize("2xx.txt") > 0:
        timeheader = f"-H '{args.header}'" if args.header else ""
        if args.threads:
            nucl = f"nuclei -l 2xx.txt -rl {args.threads} {timeheader} -o nuclei.txt -jsonl-export nuclei.json"
        else:
            nucl = f"nuclei -l 2xx.txt {timeheader} -o nuclei.txt -jsonl-export nuclei.json"
        run_silent(nucl, "Running Nuclei scan")
    else:
        print(f"{Y}[!] 2xx.txt is empty or missing. Skipping Nuclei.{C}")

# Subzy
if args.subzy:
    if os.path.exists("sort.txt") and os.path.getsize("sort.txt") > 0:
        subz = "subzy run --targets sort.txt > subzy.json"
        run_silent(subz, "Running Subzy takeover scan")
    else:
        print(f"{Y}[!] sort.txt is empty. Skipping Subzy.{C}")

script_end = time.time()
total_duration = script_end - total_start

print(f"[!] Recon complete! Results are sorted. Run 'ls' to see the files.")
