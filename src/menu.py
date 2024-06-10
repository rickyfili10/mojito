import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44
import time
import os
from scapy.all import *

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

# Create blank image for drawing
width = 128
height = 128
image = Image.new('RGB', (width, height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

# Menu options
menu_options = ["Test", "Reboot", "Shutdown", "Sniff WiFi"]
selected_index = 0

def draw_menu(selected_index):
    # Clear previous image
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    
    for i, option in enumerate(menu_options):
        y = i * 20  # Spacing between menu items
        draw.text((1, y), option, font=font, fill=(255, 255, 255))
        if i == selected_index:
            text_size = draw.textbbox((1, y), option, font=font)
            draw.line((1, y + text_size[3] - text_size[1], 1 + text_size[2] - text_size[0], y + text_size[3] - text_size[1]), fill=(0, 255, 0))
    
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
        return f"IP: {dst_ip}, Port: {dst_port}"

# Function to sniff WiFi packets
def sniff_wifi():
    sniff(iface="wlan0", filter="tcp", prn=lambda x: show_message(packet_handler(x), 1))

draw_menu(selected_index)  # Initial draw

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
            elif menu_options[selected_index] == "Test":
                # Show "Hello World" for 3 seconds
                show_message("Hello World", 3)
                # Redraw menu after message
                draw_menu(selected_index)
            elif menu_options[selected_index] == "Sniff WiFi":
                # Sniff WiFi packets
                sniff_wifi()
                # Redraw menu after sniffing
                draw_menu(selected_index)
            # Debounce delay
            time.sleep(0.3)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
