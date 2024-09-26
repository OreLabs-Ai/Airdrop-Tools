import random
import os
import time
from pyrogram import Client
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

def read_api_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    api_data = [line.strip().split() for line in lines]
    return api_data

def read_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file.readlines()]
    return proxies

def parse_proxy(proxy_url):
    parsed = urlparse(proxy_url)
    return {
        'scheme': parsed.scheme,
        'hostname': parsed.hostname,
        'port': parsed.port
    }

def sanitize_filename(filename):
    return ''.join(c for c in filename if c.isalnum() or c in (' ', '_')).rstrip()

def main():
    api_data = read_api_data('api.txt')
    proxies = read_proxies('proxies.txt')

    if not api_data:
        print("Error: No API data found in api.txt")
        return

    if not proxies:
        print("Error: No proxies found in proxies.txt")
        return

    while True:
        # Pilih API ID dan API Hash secara acak
        api_id, api_hash = random.choice(api_data)
        
        # Pilih proxy secara acak
        proxy_url = random.choice(proxies)
        proxy = parse_proxy(proxy_url)

        print(f"{Fore.CYAN}{Style.BRIGHT}Menggunakan API ID: {api_id}")
        print(f"{Fore.CYAN}{Style.BRIGHT}Menggunakan proxy: {proxy_url}")

        # Tanya pengguna untuk aktifkan atau nonaktifkan proxy
        proxy_choice = input(f"{Fore.CYAN}{Style.BRIGHT}Aktifkan proxy? (y/n): ").strip().lower()
        if proxy_choice == 'n':
            proxy = None
            print(f"{Fore.RED}{Style.BRIGHT}Proxy dinonaktifkan.")

        # Buat folder sessions jika belum ada
        os.makedirs('sessions', exist_ok=True)

        temp_session_name = "sessions/temp_session"

        # Buat instance Client Pyrogram dengan nama sementara
        app = Client(
            temp_session_name,
            api_id=api_id,
            api_hash=api_hash,
            proxy=proxy
        )

        # Jalankan client
        try:
            with app:
                print(f"{Fore.GREEN}{Style.BRIGHT}Berhasil terhubung!")
                me = app.get_me()
                print(f"{Fore.GREEN}{Style.BRIGHT}Anda masuk sebagai {me.first_name} (ID: {me.id})")
                
                # Buat nama file sesi baru berdasarkan first name
                safe_name = sanitize_filename(me.first_name.lower())
                new_session_name = f"sessions/{safe_name}.session"

            # Rename file sesi
            old_session_file = f"{temp_session_name}.session"
            new_session_file = new_session_name
            
            if os.path.exists(old_session_file):
                os.rename(old_session_file, new_session_file)
                print(f"{Fore.GREEN}{Style.BRIGHT}File sesi disimpan sebagai: {new_session_file}")
            else:
                print(f"{Fore.YELLOW}{Style.BRIGHT}Peringatan: File sesi {old_session_file} tidak ditemukan.")
        
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Terjadi kesalahan: {e}")

        # Tanya pengguna untuk pendaftaran baru
        repeat = input(f"{Fore.CYAN}{Style.BRIGHT}Daftarkan nomor baru? (y/n): ").strip().lower()
        if repeat != 'y':
            break

if __name__ == "__main__":
    main()