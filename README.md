# STILL UNDER DEVELOPMENT 👨‍💻
### Ehy! We are working hard on this project! So please if you can help us! 🫰
## No release will be made before version 1.0. Using the code now may have bugs or incomplete pieces. ❌💿

# The Mojito Project by Blackat 🍹

## Why is called "mojito" like the cocktail? 🍸
This project is called "Mojito" beacuse while the developers were coding this project, they were drinking non-alcoholic mojitos (maked by @rickyfili10)
![mojito](https://github.com/user-attachments/assets/b10b95f5-7286-47bb-a8e1-64bc07b0ffd4)

# What's that? 🤔
Mojito is an penetration testing project created only for educational purposes and runs on a raspberry pi 0 w/wh that use a wavseshare 1.44 inch lcd HAT display. It have a collection of hacking tools and it is based on Kali Linux. 

# DISCLAIMER ⚠️
### Mojito is for educational purposes only. 📝
The authors take NO responsibility and liability for how you use any of the tools/source code/any files provided. The authors and anyone affiliated with will not be liable for any losses and/or damages in connection or other type of damages with use of ANY Tools provided with Mojito. DO NOT use Mojito if you don't have the permission to do that. <br>

## USE IT AT YOUR OWN RISK. 🫵
# REQUIREMENTS 📃
  - Wavseshare 1.44 inch lcd HAT display 📱
  - Raspberry pi 0 w/wh 💻
  - 32 GB sd card (You need much less, but you might need 32 GB in the future for other projects!) 📀
# HOW TO SETUP AND INSTALL MOJITO? 🔧
1. Flash and setup kali linux for raspberry pi 0 wh 💿
2. Install and setup requisites with the commands below 🔧
## Clone the Mojito repostory and enter in it 🐈‍⬛🍹
 ```
  git clone https://github.com/rickyfili10/mojito.git && cd mojito/src
 ```
## Install the requisites 📃
 ```
    sudo apt update
    sudo apt-get install libbluetooth-dev
    sudo apt install python3-spidev python3-RPi.gpio
    sudo pip install git+https://github.com/pybluez/pybluez 
```
   ### <br>Set the time zone ⌚
```
    sudo timedatectl set-timezone {your local time zone} -- EXAMPLE FOR ITALY: "sudo timedatectl set-timezone Europe/Rome"
```
  ### Install l2ping ⛓️‍💥
```
    sudo apt install l2ping 
```
   ## Use "sudo raspi-config" and enable SPi interface ⚠️
   ### Install wget ⬇️
```
 sudo apt install wget
```
   ### Download hamachi for make party ⬇️
```
 wget https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_armel.deb
```
  ### Install hamachi ⬇️ 
```
  sudo dpkg -i logmein-hamachi_2.1.0.203-1_armel.deb
```
  ### Execute Mojito at boot ⏰
```
  sudo cp mojito.service /etc/systemd/system/
```
```
 sudo systemctl daemon-reload
```
```
  sudo systemctl enable mojito.service
```
```
  sudo systemctl start mojito.service
```
```
  sudo reboot
```

## After a while it should display the Mojito menu! 🎉
# SIMBOLS LIST: ☯️
   - NB! = No Battery Found! 🙅‍♂️<br> 
   - Plug = pluged to a power source 🔌<br>
   - N% = battery level ( not tested ) 🔋<br>
# TO DO ✔️
  [<br>
  ❌ Not implemented yet <br>
  ✔️ Implemented <br>
  ✏️ Almost implemented or in development<br>
  🔧 Dosen't work and should be fixed<br>
  ⌚ In pause for now<br>
  ⚒️ To fix soon<br>
  🛑 End of support<br>
  ]
   - ❌ Add wifi deauth
   - ❌ Add wifi sniff
   - ❌ Add wifi beacon
   - ✔️ Fix I/O errors
   - ❌ Add Apple sideload (probably impossible)
   - ⌚ Add Apple Jailbreaker (like checkra1n and dopamine)
   - ❌ Add adb apk installer (for bypass family link (if you are a kid 🤣🫵) or to bypass blocks on company phones)
   - ❌ Add android rooter -> Bootloader unlocker, vbmeta flasher and sudo binary flasher (like Magisk)
   - ✏️ Mojito official wiki
   - 🔧 Fix Settings app
   - ⚒️ Fix that you can't use iOs bluetooth spam more than 1 time
   - ⚒️ Fix all the exit and link KEY1, KEY2 & KEY3 for exit when you press it
   - ✏️ Put all the libraries in libs folder to make the code cleaner
   - ⌚ Add party function
   - ❌ Add a function to save Wifi and Wifi password to connect to networks without password
   - ✔️ Plugin and app support (Plugin support can be bugged)

### Under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) Licence 📄
  What you can do: ✔️<br>
   - Share 🔗<br>
   - Use for non-commercial purposes 💸❌<br>
   - Creating Derivative Works --> Theoretically under this license you couldn't, but the authors decided that you can do it anyway. As long as you will pubblicate the source code and if the authors don't like what you did you will be forced to remove it ✔️<br>
  What you can't do: ❌<br>
   - Impose additional restrictions 🟰<br>

Screen drivers based on https://github.com/Kudesnick/1.44inch-LCD-HAT-Code 💻<br>

## --- By BlacKat team. ツ --- 🐈‍⬛
# Please follow us and drop a star! ⭐
