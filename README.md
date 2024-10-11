# STILL UNDER DEVELOPMENT
# The Mojito Project by Blackat
<br>![logo](https://github.com/rickyfili10/mojito/blob/main/logo.png)
## Why is called "mojito" like the cocktail?
This project is called "Mojito" beacuse while the developers were coding this project, they were drinking mojitos (maked by @rickyfili10)

# What's that?
Mojito is an penetration testing project created only for educational purposes and runs on a raspberry pi 0 w/wh that use a wavseshare 1.44 inch lcd HAT display. It have a collection of hacking tools and it is based on Kali Linux. 

# DISCLAIMER
### Mojito is for educational purposes only.
The authors take NO responsibility and liability for how you use any of the tools/source code/any files provided. The authors and anyone affiliated with will not be liable for any losses and/or damages in connection or other type of damages with use of ANY Tools provided with Mojito. DO NOT use Mojito if you don't have the permission to do that. 
### USE IT AT YOUR OWN RISK.

# HOW TO SETUP AND INSTALL MOJITO?
1. Flash and setup kali linux for raspberry pi 0 wh
2. Clone Mojito repostory
3. Install and setup requisites using
   - "sudo pip install pybluez spidev RPi.gpio l2ping" if pybluez dosen't install --> sudo pip install git+https://github.com/pybluez/pybluez
   - use sudo raspi-config to enable SPi interface
   - sudo apt update && sudo apt install wget
   - wget https://www.vpn.net/installers/logmein-hamachi-2.1.0.203-1.armel.rpm
   - sudo rpm -ivh logmein-hamachi-2.1.0.203-1.armel.rpm
   - sudo cp mojito.services /etc/systemd/system/
   - sudo systemctl daemon-reload
   - sudo systemctl enable mojito.services
   - sudo systemctl start mojito.services
   - sudo reboot
  After a while it should display the Mojito menu.


--- With love by BlacKat team. ツ ---

Screen drivers based on https://github.com/Kudesnick/1.44inch-LCD-HAT-Code
