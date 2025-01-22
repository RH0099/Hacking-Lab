import os
import subprocess
import qrcode
from cryptography.fernet import Fernet
import psutil
from PIL import Image
import pytesseract
import json

def banner():
    print("=" * 50)
    print("           Ultimate Termux Toolkit (UTT)            ")
    print("=" * 50)

def menu():
    print("\nChoose an option:")
    print("1. Basic Network Scan")
    print("2. Advanced Network Scan")
    print("3. QR Code Generator")
    print("4. File Encryption/Decryption")
    print("5. Device Resource Monitoring")
    print("6. Text Extraction from Image")
    print("7. Hide File in Image")
    print("8. Extract File from Image")
    print("9. Hide Executable in Image")
    print("10. Exit")
    return input("\nEnter your choice: ")

# Option 1: Basic Network Scan
def basic_network_scan():
    print("\n[+] Scanning basic WiFi information...")
    try:
        result = subprocess.check_output("termux-wifi-connectioninfo", shell=True).decode("utf-8")
        print("\n[+] Current Network Info:")
        print(result)
    except Exception as e:
        print(f"[-] Error: {e}")

# Option 2: Advanced Network Scan
def advanced_network_scan():
    print("\n[+] Scanning available networks...")
    try:
        result = subprocess.check_output("termux-wifi-scaninfo", shell=True).decode("utf-8")
        networks = json.loads(result)
        if networks:
            print("\n[+] Available Networks:")
            for network in networks:
                print(f"SSID: {network['ssid']}")
                print(f"BSSID: {network['bssid']}")
                print(f"Signal Strength: {network['signal_level']} dBm")
                print(f"Encryption: {network['capabilities']}")
                print("-" * 40)
        else:
            print("[-] No networks found. Try again later.")
    except Exception as e:
        print(f"[-] Error: {e}")

# Option 3: QR Code Generator
def generate_qr():
    data = input("\nEnter the data to generate QR code: ")
    filename = input("Enter filename to save QR code (e.g., qr.png): ")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)
    print(f"[+] QR Code saved as {filename}")

# Option 4: File Encryption/Decryption
def encrypt_file():
    def generate_key():
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key():
        return open("secret.key", "rb").read()

    choice = input("\nDo you want to (E)ncrypt or (D)ecrypt a file? ").lower()
    if choice == "e":
        generate_key()
        key = load_key()
        f = Fernet(key)
        filename = input("Enter the filename to encrypt: ")
        with open(filename, "rb") as file:
            encrypted_data = f.encrypt(file.read())
        with open(filename, "wb") as file:
            file.write(encrypted_data)
        print("[+] File encrypted successfully!")
    elif choice == "d":
        key = load_key()
        f = Fernet(key)
        filename = input("Enter the filename to decrypt: ")
        with open(filename, "rb") as file:
            decrypted_data = f.decrypt(file.read())
        with open(filename, "wb") as file:
            file.write(decrypted_data)
        print("[+] File decrypted successfully!")
    else:
        print("[-] Invalid choice!")

# Option 5: Device Resource Monitoring
def device_monitor():
    print("\n[+] Device Resource Monitoring:")
    print(f"CPU Usage: {psutil.cpu_percent()}%")
    print(f"Memory Usage: {psutil.virtual_memory().percent}%")
    print(f"Disk Usage: {psutil.disk_usage('/').percent}%")
    battery = psutil.sensors_battery()
    if battery:
        print(f"Battery: {battery.percent}%")
    else:
        print("Battery information unavailable.")

# Option 6: Text Extraction from Image
def text_extraction():
    image_path = input("\nEnter the image path for text extraction: ")
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        print("\n[+] Extracted Text:")
        print(text)
    except Exception as e:
        print(f"[-] Error: {e}")

# Option 7: Hide File in Image
def hide_file_in_image():
    print("\n[+] File Hiding in Image")
    try:
        image_path = input("Enter the image file path (e.g., image.png): ")
        file_to_hide = input("Enter the file to hide (e.g., secret.txt): ")
        output_image = input("Enter the output image name (e.g., output.png): ")

        with open(file_to_hide, "rb") as file:
            data = file.read()

        with open(image_path, "rb") as img:
            img_data = img.read()

        with open(output_image, "wb") as out_img:
            out_img.write(img_data + b"STEGA" + data)

        print(f"[+] File successfully hidden in {output_image}")
    except Exception as e:
        print(f"[-] Error: {e}")

# Option 8: Extract File from Image
def extract_file_from_image():
    print("\n[+] Extracting File from Image")
    try:
        image_path = input("Enter the image file path with hidden data (e.g., output.png): ")
        output_file = input("Enter the name to save extracted file (e.g., extracted.txt): ")

        with open(image_path, "rb") as img:
            img_data = img.read()

        if b"STEGA" in img_data:
            file_data = img_data.split(b"STEGA")[1]

            with open(output_file, "wb") as file:
                file.write(file_data)

            print(f"[+] Hidden file extracted and saved as {output_file}")
        else:
            print("[-] No hidden file found in the image.")
    except Exception as e:
        print(f"[-] Error: {e}")

# Option 9: Hide Executable in Image
def hide_executable_in_image():
    print("\n[+] Hiding Executable in Image")
    try:
        image_path = input("Enter the image file path (e.g., image.jpg): ")
        executable_path = input("Enter the executable file path (e.g., payload.bat): ")
        output_file = input("Enter the output file name (e.g., combined.jpg): ")

        with open(image_path, "rb") as img_file:
            img_data = img_file.read()
        with open(executable_path, "rb") as exe_file:
            exe_data = exe_file.read()

        with open(output_file, "wb") as out_file:
            out_file.write(img_data + b"EXEHIDE" + exe_data)

        print(f"[+] Executable hidden in {output_file}. Rename to .exe or .bat to run.")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    banner()
    while True:
        choice = menu()
        if choice == "1":
            basic_network_scan()
        elif choice == "2":
            advanced_network_scan()
        elif choice == "3":
            generate_qr()
        elif choice == "4":
            encrypt_file()
        elif choice == "5":
            device_monitor()
        elif choice == "6":
            text_extraction()
        elif choice == "7":
            hide_file_in_image()
        elif choice == "8":
            extract_file_from_image()
        elif choice == "9":
            hide_executable_in_image()
        elif choice == "10":
            print("\n[+] Exiting... Goodbye!")
            break

if __name__ == "__main__":
    main()
