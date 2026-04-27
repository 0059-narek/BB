# 0059 RECON 🚀

A powerful automation script for subdomain enumeration, filtering, and status code categorization.

## ⚙️ Features
- **Multi-Tool Discovery**: Runs `subfinder`, `assetfinder`, and `sublist3r` simultaneously.
- **Auto-Deduplication**: Merges results and removes duplicate subdomains.
- **Live Host Probing**: Uses `httpx` to verify live targets and fetch titles/tech stack.
- **Smart Sorting**: Automatically sorts results into `2xx.txt`, `3xx.txt`, `4xx.txt`, and `5xx.txt`.
- **Silent Execution**: Clean UI with progress tracking.

## 🛠 Prerequisites
Ensure you have the following installed and in your PATH:
- [subfinder](https://github.com/projectdiscovery/subfinder)
- [assetfinder](https://github.com/tomnomnom/assetfinder)
- [sublist3r](https://github.com/aboul3la/Sublist3r)
- [httpx](https://github.com/projectdiscovery/httpx)
- [nuclei](https://github.com/projectdiscovery/nuclei.git)
- [subzy](https://github.com/PentestPad/subzy.git)

## 🚀 Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/0059-narek/recon.git](https://github.com/0059-narek/recon.git)
   cd recon
