import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import LCD_1in44
import time
import os
import subprocess
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Pin setup
KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(KEY3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize display
disp = LCD_1in44.LCD()
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDir)
disp.LCD_Clear()








def list_files_in_directory(directory):
    """List all files in the specified directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def draw_file_menu(files, selected_index):
    """Draw the file menu on the display in a grid format."""
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    
    # Definire dimensioni della griglia
    num_cols = 3  # Numero di colonne
    num_rows = 4  # Numero di righe
    item_width = width // num_cols
    item_height = 20  # Altezza dell'elemento, puoi modificarlo se necessario
    
    for i, file in enumerate(files):
        col = i % num_cols
        row = i // num_cols
        x = col * item_width
        y = row * item_height
        
        if i == selected_index:
            text_size = draw.textbbox((0, 0), file, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((x, y, x + item_width, y + item_height), fill=(0, 255, 0))  # Evidenziare lo sfondo
            draw.text((x + 1, y + 1), file, font=font, fill=(0, 0, 0))  # Testo in nero
        else:
            draw.text((x + 1, y + 1), file, font=font, fill=(255, 255, 255))  # Testo in bianco

    disp.LCD_ShowImage(image, 0, 0)


def execute_file(file_path):
    """Execute the file based on its extension."""
    if file_path.endswith('.py'):
        # For Python files
        subprocess.run(['sudo', 'python3', file_path])
    elif file_path.endswith('.sh'):
        # For shell scripts
        subprocess.run(['sudo', 'bash', file_path])
    elif file_path.endswith(".moj"):
        subprocess.run(['sudo', './', file_path])
    else:
        # Handle other types or notify user
        show_message(f"Unsupported file type: {file_path}")


def show_file_menu():
    # Supponiamo che tu abbia una directory che contiene le app o file che vuoi mostrare
    directory = "app/"  # Modifica questo percorso con il percorso corretto
    files = list_files_in_directory(directory)
    selected_index = 0
    num_cols = 3  # Numero di colonne
    num_rows = 4  # Numero di righe

    def draw_file_menu(files, selected_index, num_cols, num_rows):
        num_items = len(files)
        
        # Calcola le dimensioni delle celle
        cell_width = width // num_cols
        cell_height = height // num_rows

        draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

        for i, file in enumerate(files):
            y = (i // num_cols) * cell_height
            x = (i % num_cols) * cell_width
            if i == selected_index:
                draw.rectangle((x, y, x + cell_width, y + cell_height), fill=(0, 255, 0))  # Evidenzia
                draw.text((x + 2, y + 2), file, font=font, fill=(0, 0, 0))  # Testo in nero
            else:
                draw.text((x + 2, y + 2), file, font=font, fill=(255, 255, 255))  # Testo in bianco

        disp.LCD_ShowImage(image, 0, 0)

    draw_file_menu(files, selected_index, num_cols, num_rows)

    while True:
        if GPIO.input(KEY_UP_PIN) == 0:
            selected_index = (selected_index - num_cols) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_DOWN_PIN) == 0:
            selected_index = (selected_index + num_cols) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_LEFT_PIN) == 0:
            selected_index = (selected_index - 1) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            selected_index = (selected_index + 1) % len(files)
            draw_file_menu(files, selected_index, num_cols, num_rows)
            time.sleep(0.3)
        if GPIO.input(KEY_PRESS_PIN) == 0:
            selected_file = files[selected_index]
            show_message(f"Selected: {selected_file}", 1)
            
            # Esegui l'azione sul file selezionato
            file_path = os.path.join(directory, selected_file)
            execute_file(file_path)  # Chiamata alla funzione per eseguire il file
            break

def generate_key_from_password(password: str) -> bytes:
    """Genera una chiave AES a partire dalla password."""
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(message: str, key: bytes) -> bytes:
    """Cripta un messaggio usando una chiave e restituisce il testo cifrato."""
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_message = padder.update(message.encode()) + padder.finalize()
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return iv + encrypted_message

def write_encrypted_message_to_file(file_path: str, message: str, key: bytes):
    """Cripta un messaggio e lo scrive in un file."""

    encrypted_message = encrypt_message(message, key)
    with open(file_path, 'wb') as file:
        file.write(encrypted_message)
def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decifra un messaggio usando una chiave e restituisce il testo in chiaro."""
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        message = unpadder.update(padded_message) + unpadder.finalize()
        return message.decode()
    except ValueError:
        pass
def setPsk():
    # Definisci il messaggio da criptare e la chiave per la cifratura
    original_message = "mojito"
    show_message("Create a password:", 3)
    password = get_keyboard_input()  # Password per generare la chiave AES
    key = generate_key_from_password(password)

    # Scrivi il messaggio criptato nel file psk.txt
    write_encrypted_message_to_file("psk.txt", original_message, key)
    show_message("Password Saved.", 3)
def read_encrypted_message_from_file(file_path: str) -> bytes:
    """Legge un messaggio criptato da un file."""
    with open(file_path, 'rb') as file:
        return file.read()
def returner():
    psk_try = 0
    max_tries = 4
    if os.path.exists("psk.txt"):
        encrypted_message = read_encrypted_message_from_file("psk.txt")

        while psk_try < max_tries:
            show_message("Password Required.", 1)
            user_password = get_keyboard_input()
            user_key = generate_key_from_password(user_password)

            try:
                decrypted_message = decrypt_message(encrypted_message, user_key)

                if decrypted_message == "mojito":
                    show_message("Login in...", 1)
                    break

                else:
                    show_message("Wrong password", 1)
                    psk_try += 1
            except ValueError as e:
                show_message(str(e))
                psk_try += 1


    else:
        setPsk()



































# Display logo at startup


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

        # Verifica dell'input dei tasti speciali
        if GPIO.input(KEY1_PIN) == 0:  # Se KEY1 (P21) è premuto, cancella l'ultimo carattere
            input_text = input_text[:-1]
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)
        
        if GPIO.input(KEY2_PIN) == 0:  # Se KEY2 (P20) è premuto, aggiungi uno spazio
            input_text += ' '
            draw_keyboard(selected_key_index, input_text, mode, caps_lock)
            time.sleep(0.3)

        if GPIO.input(KEY3_PIN) == 0:  # Se KEY3 (P16) è premuto, conferma l'input
            return input_text

        # Gestione dell'input del pulsante di selezione (KEY_PRESS_PIN)
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
menu_options = ["Networks","Bluetooth", "Payload", "Party", "App & Plugin", "Shutdown"]
selected_index = 0
def show_image(image_path, exit_event=None):
    image = Image.open(image_path)
    image = image.resize((128, 128))  # Resize the image to fit the display if necessary

    disp.LCD_Clear()  # Clear the display
    disp.LCD_ShowImage(image, 0, 0)  # Show the image on the display

    # Wait for exit event (e.g., button press or timeout)
    while True:
        if exit_event is not None and exit_event():
            break  # Exit the loop if exit event occurs
        time.sleep(0.1)  # Adjust sleep time as needed

    disp.LCD_Clear()  # Clear the display after exit

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
    disp.LCD_Clear()

returner()

while True:
    listen_for_messages()
    data, addr = socket.recvfrom(1024)  # Dimensione buffer
    show_message(f"\n[{addr}]\n{data.decode('utf-8')}", 3)
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
                        sub_menu_options = ["Fake AP"]
                        sub_selected_index = 0

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

                                if sub_selected_option == "Fake AP":
                                    show_message("Create a name for\n the fake AP", 3)
                                    fakeAp = get_keyboard_input()
                                    os.system(f"sudo wifiphisher -e {fakeAp}")
                                    show_image("fakeAp.png", lambda: GPIO.input(KEY_PRESS_PIN) == 0)  # Show image until button press

                     # Exit sub-menu to main menu

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
            sub_menu_options = ["Spam"]
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

                    if sub_selected_option == "Spam":
                        sub_menu_options = ["iOS"]
                        sub_selected_index = 0

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

                                if sub_selected_option == "iOS":
                                    os.system("sudo python3 iphone.py")
                                    show_image("bkat.png", lambda: GPIO.input(KEY_PRESS_PIN) == 0)  # Show image until button press

                    break  # Exit Bluetooth menu to main menu



        elif selected_option == "App & Plugin":
            show_file_menu()  # Call the function to show files







        elif selected_option == "Payload":
            # Add your logic here for Payload option
            show_message("Opening Payload Settings...", 2)
        elif selected_option == "Shutdown":
            show_message("Shutting down...", 2)
            time.sleep(1)
            subprocess.call(['sudo', 'shutdown', '-h', 'now'])
        else:
            show_message("Unknown option", 2)
