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

def draw_keyboard(selected_key_index, input_text, mode="alpha", caps_lock=False):
    if mode == "alpha":
        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
            ' ', 'DEL', '⏎', "!#1", "CAPS"
        ]
    else:  # special characters mode
        keys = [
            '!', '"', '£', '$', '%', '&', '/', '(', ')', '=',
            '?', '^', '@', '#', '_', '-', '+', '{', '}', '\\',
            '[', ']', '*', ':', ';', "'", '<', '>', '|', '~',
            ' ', 'DEL', '⏎', "ABC", "CAPS"
        ]
    
    if caps_lock:
        keys = [key.upper() if key.isalpha() else key for key in keys]
    
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
    alpha_keys = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';',
        'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/',
        ' ', 'DEL', '⏎', "!#1", "CAPS"
    ]
    special_keys = [
        '!', '"', '£', '$', '%', '&', '/', '(', ')', '=',
        '?', '^', '@', '#', '_', '-', '+', '{', '}', '\\',
        '[', ']', '*', ':', ';', "'", '<', '>', '|', '~',
        ' ', 'DEL', '⏎', "ABC", "CAPS"
    ]
    
    input_text = ""
    selected_key_index = 0
    mode = "alpha"
    caps_lock = False
    
    draw_keyboard(selected_key_index, input_text, mode, caps_lock)
    
    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            selected_key_index = (selected_key_index - 10) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_DOWN_PIN) == 0:
            selected_key_index = (selected_key_index + 10) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_LEFT_PIN) == 0:
            selected_key_index = (selected_key_index - 1) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            selected_key_index = (selected_key_index + 1) % len(alpha_keys)
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        if GPIO.input(KEY_PRESS_PIN) == 0:
            key = alpha_keys[selected_key_index] if mode == "alpha" else special_keys[selected_key_index]
            if key == "DEL":
                input_text = input_text[:-1]
            elif key == "⏎":
                return input_text
            elif key == "!#1":
                mode = "special" if mode == "alpha" else "alpha"
            elif key == "CAPS":
                caps_lock = not caps_lock
            else:
                input_text += key.upper() if caps_lock else key
            
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)

# Menu options
menu_options = ["Networks", "Bluetooth", "Payload", "Party", "Reboot", "Shutdown"]
selected_index = 0

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

def show_message(message, duration=2):
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))  # Clear previous image
    draw.text((10, 50), message, font=font, fill=(255, 255, 255))
    disp.LCD_ShowImage(image, 0, 0)
    time.sleep(duration)

while True:
    draw_menu(selected_index)
    
    if GPIO.input(KEY_UP_PIN) == 0:
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)
    if GPIO.input(KEY_DOWN_PIN) == 0:
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu(selected_index)
        time.sleep(0.3)
    if GPIO.input(KEY_PRESS_PIN) == 0:
        selected_option = menu_options[selected_index]
        show_message(f"Selected: {selected_option}", 1)
        
        if selected_option == "Networks":
            # Draw and handle the Network sub-menu
            sub_menu_options = ["Wifi", "Deauth", "Firewall"]
            sub_selected_index = 0
            
            def draw_sub_menu(sub_selected_index):
                draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                for i, option in enumerate(sub_menu_options):
                    y = i * 20
                    if i == sub_selected_index:
                        text_size = draw.textbbox((0, 0), option, font=font)
                        text_width = text_size[2] - text_size[0]
                        text_height = text_size[3] - text_size[1]
                        draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0))
                        draw.text((1, y), option, font=font, fill=(0, 0, 0))
                    else:
                        draw.text((1, y), option, font=font, fill=(255, 255, 255))
                disp.LCD_ShowImage(image, 0, 0)
            
            while True:
                draw_sub_menu(sub_selected_index)
                
                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    show_message(f"Selected: {sub_selected_option}", 1)
                    
                    if sub_selected_option == "Wifi":
                        # Add your logic here for Wifi option

                        # Pause before allowing further input
                        time.sleep(1)
                    elif sub_selected_option == "Deauth":
                        os.system("airmon-ng start wlan0")
                        time.sleep(1)
                    
                    break  # Exit sub-menu to main menu
        elif selected_option == "Party":
            # Draw and handle the Network sub-menu
            sub_menu_options = ["Login", "Join a Party", "Create a Party", "Leave Party", "Exit"]
            sub_selected_index = 0
            
            def draw_sub_menu(sub_selected_index):
                draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                for i, option in enumerate(sub_menu_options):
                    y = i * 20
                    if i == sub_selected_index:
                        text_size = draw.textbbox((0, 0), option, font=font)
                        text_width = text_size[2] - text_size[0]
                        text_height = text_size[3] - text_size[1]
                        draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0))
                        draw.text((1, y), option, font=font, fill=(0, 0, 0))
                    else:
                        draw.text((1, y), option, font=font, fill=(255, 255, 255))
                disp.LCD_ShowImage(image, 0, 0)
            
            while True:
                draw_sub_menu(sub_selected_index)
                
                if GPIO.input(KEY_UP_PIN) == 0:
                    sub_selected_index = (sub_selected_index - 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index)
                    time.sleep(0.3)
                if GPIO.input(KEY_DOWN_PIN) == 0:
                    sub_selected_index = (sub_selected_index + 1) % len(sub_menu_options)
                    draw_sub_menu(sub_selected_index)
                    time.sleep(0.3)
                if GPIO.input(KEY_PRESS_PIN) == 0:
                    sub_selected_option = sub_menu_options[sub_selected_index]
                    show_message(f"Selected: {sub_selected_option}", 1)
                    
                    if sub_selected_option == "Join a Party":
                        show_message("Select the party name", 3)
                        partyName = get_keyboard_input()
                        show_message("Select the password of party", 3)
                        partyPassword = get_keyboard_input()
                        # Esegui il comando usando subprocess.run per ottenere l'output
                        result = subprocess.run(["sudo", "hamachi", "join", partyName, partyPassword], capture_output=True, text=True)
                        show_message(result.stdout, 3)
                        time.sleep(1)
                    elif sub_selected_option == "Create a Party":
                        show_message("Create a party name", 3)
                        CpartyName = get_keyboard_input()
                        show_message("Create a password", 3)
                        CpartyPassword = get_keyboard_input()
                        # Esegui il comando usando subprocess.run per ottenere l'output
                        result = subprocess.run(["sudo", "hamachi", "create", CpartyName, CpartyPassword], capture_output=True, text=True)
                        show_message(result.stdout, 3)
                        time.sleep(1)
                    elif sub_selected_option == "Login":
                        result = subprocess.run(["sudo", "login"], capture_output=True, text=True)
                        show_message(result.stdout, 3)
                    elif sub_selected_option == "Leave Party":
                        show_message("Write the party name\nto confirm leaving", 3)
                        LpartyName = get_keyboard_input()
                        result = subprocess.run(["sudo", "hamachi", "leave", LpartyName,], capture_output=True, text=True)
                        show_message(result.stdout, 3)
                    
                    
                    break  # Exit sub-menu to main menu
        elif selected_option == "Bluetooth":
            # Add your logic here for Bluetooth option
            show_message("Opening Bluetooth Settings...", 2)
        elif selected_option == "Payload":
            # Add your logic here for Payload option
            show_message("Opening Payload Settings...", 2)
        elif selected_option == "Passwords":
            password = get_keyboard_input()
            show_message(f"Password: {password}", 3)
        elif selected_option == "Reboot":
            show_message("Rebooting...", 2)
            time.sleep(1)
            subprocess.call(['sudo', 'reboot'])
        elif selected_option == "Shutdown":
            show_message("Shutting down...", 2)
            time.sleep(1)
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        else:
            show_message("Unknown option", 2)
