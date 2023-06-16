import requests
import subprocess
from bs4 import BeautifulSoup
import os
import sys
import argparse

def cmd(command):
  p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err= p.communicate()
  return out, err

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Installation")
    parser.add_argument("args", choices=["32", "64"], help="32 or 64")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    args=parser.parse_args()
    
    cmd("sudo apt update && sudo apt upgrade -y")
    cmd("sudo apt install git -y")
    cmd("git clone https://github.com/thiagoralves/OpenPLC_v3.git")
    url="https://github.com/WiringPi/WiringPi/releases/"
    r=requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        find_class=soup.find_all(class_="ml-1 wb-break-all")
        for value in find_class:
            value=str(value.string)
            value=value.strip()
    else:
        print("Error:", r.status_code)

    download_url_32=f"https://github.com/WiringPi/WiringPi/releases/download/{value}/wiringpi-{value}-armhf.deb"
    download_url_64=f"https://github.com/WiringPi/WiringPi/releases/download/{value}/wiringpi-{value}-arm64.deb"
    if sys.argv[1] == "32":
        cmd(f"wget {download_url_32} -O wiringpi-{value}-32.deb")
        cmd(f"dpkg -i wiringpi-{value}-32.deb")
    if sys.argv[1] == "64":
        cmd(f"wget{download_url_64} -O wiringpi-{value}-64.deb")
        cmd(f"dpkg -i wiringpi-{value}-64.deb")

    os.chdir("OpenPLC_v3")
    cmd("sudo ./install.sh rpi")
