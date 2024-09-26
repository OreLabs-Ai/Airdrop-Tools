import os
import random
import sys
from telethon.sync import TelegramClient
from telethon.errors import PhoneNumberInvalidError, SessionPasswordNeededError, AuthRestartError, PasswordHashInvalidError
from colorama import Fore, Style, init

init(autoreset=True)

def read_api_data(file_path='api.txt'):
    api_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    try:
                        api_data.append((int(parts[0]), parts[1]))
                    except ValueError:
                        print(f"{Fore.RED}[X] Invalid API ID in {file_path}. Skipping line.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}[X] {file_path} file not found. Using default API.{Style.RESET_ALL}")
    return api_data

def read_proxies(file_path='proxies.txt'):
    proxies = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                proxy = line.strip()
                if proxy:
                    parts = proxy.split('://')
                    proxy_type, proxy_addr = (parts[0], parts[1]) if len(parts) == 2 else ('http', parts[0])
                    try:
                        ip, port = proxy_addr.split(':')
                        proxies.append({
                            'proxy_type': proxy_type,
                            'addr': ip,
                            'port': int(port),
                            'rdns': True
                        })
                    except ValueError:
                        print(f"{Fore.RED}[X] Invalid proxy format in {file_path}. Skipping line.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}[X] {file_path} file not found. Proxies are required.{Style.RESET_ALL}")
        sys.exit(1)
    if not proxies:
        print(f"{Fore.RED}[X] No valid proxies found in {file_path}. Proxies are required.{Style.RESET_ALL}")
        sys.exit(1)
    return proxies

def random_api(api_data):
    return random.choice(api_data) if api_data else (25322685, 'e33399af84db8f3c6ab1e8a50ac91d02')

def validate_phone_number(phone_number):
    return phone_number.startswith('+') and len(phone_number) > 1

def print_proxy_status(proxy, status):
    print(f"{Fore.CYAN}[#] Proxy {status}: {proxy['proxy_type']}://{proxy['addr']}:{proxy['port']}{Style.RESET_ALL}")

def sign_in_with_2fa(client, phone_number, code):
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            client.sign_in(phone_number, code)
            print(f"{Fore.GREEN}[✓] Successfully signed in!{Style.RESET_ALL}")
            return True
        except SessionPasswordNeededError:
            print(f"{Fore.YELLOW}[!] Two-Factor Authentication is enabled.{Style.RESET_ALL}")
            password = input(f"{Fore.GREEN}[+] Enter your 2FA password: {Style.RESET_ALL}")
            try:
                client.sign_in(password=password)
                print(f"{Fore.GREEN}[✓] Successfully signed in with 2FA!{Style.RESET_ALL}")
                return True
            except PasswordHashInvalidError:
                print(f"{Fore.RED}[X] Invalid 2FA password. Attempts left: {max_attempts - attempt - 1}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}[X] Failed to sign in after {max_attempts} attempts.{Style.RESET_ALL}")
    return False

def main():
    api_data = read_api_data()
    proxies = read_proxies()

    while True:
        try:
            phone_number = input(f"{Fore.YELLOW}{Style.BRIGHT}[+] Input your number (Ex: +62): ")
            if not validate_phone_number(phone_number):
                print(f"{Fore.RED}[X] Invalid phone number format. Please use international format (e.g., +62123456789).{Style.RESET_ALL}")
                continue

            use_proxy = input(f"{Fore.YELLOW}[+] Do you want to use a proxy? (y/n): ").strip().lower()
            if use_proxy == 'y':
                proxy = random.choice(proxies)
                print_proxy_status(proxy, "Active")
                proxy_config = proxy
            else:
                print(f"{Fore.GREEN}[#] Proxy not used{Style.RESET_ALL}")
                proxy_config = None

            session_name = phone_number.replace('+', '_')
            session_folder = 'sessions'
            session_path = os.path.join(session_folder, session_name + '.session')

            if os.path.exists(session_path):
                print(f"{Fore.YELLOW}[#] You already have a session with this number.{Style.RESET_ALL}")
                print(Fore.LIGHTCYAN_EX + "=" * 56 + Style.RESET_ALL)
                continue

            api_id, api_hash = random_api(api_data)
            print(f"{Fore.WHITE}{Style.BRIGHT}[#] 🔥🔥🔥 >> [{Fore.RED}{api_id}{Fore.WHITE}] {Style.RESET_ALL}")

            client = TelegramClient(session_name, api_id, api_hash, proxy=proxy_config) if proxy_config else TelegramClient(session_name, api_id, api_hash)

            max_retries = 3
            for retry in range(max_retries):
                try:
                    client.connect()
                    if not client.is_user_authorized():
                        client.send_code_request(phone_number)
                        code = input(f"{Fore.GREEN}[+] Enter the code you received: {Style.RESET_ALL}")
                        if sign_in_with_2fa(client, phone_number, code):
                            print(f"{Fore.GREEN}{Style.BRIGHT}[✓] Session Created Successfully {Style.RESET_ALL}")
                            client.disconnect()
                            os.makedirs(session_folder, exist_ok=True)
                            os.rename(session_name + '.session', session_path)
                            print(Fore.LIGHTCYAN_EX + "=" * 56 + Style.RESET_ALL)
                            break
                        else:
                            print(f"{Fore.RED}[X] Failed to create session. Please try again.{Style.RESET_ALL}")
                            break

                except AuthRestartError:
                    print(Fore.YELLOW + f"[!] Authorization process restarted by Telegram. Retrying... (Attempt {retry + 1}/{max_retries})" + Style.RESET_ALL)
                    client.disconnect()
                    if retry == max_retries - 1:
                        print(f"{Fore.RED}[X] Max retries reached. Please try again later.{Style.RESET_ALL}")
                except PhoneNumberInvalidError:
                    print(f"{Fore.RED}{Style.BRIGHT}[X] Wrong Number. Try Again...{Style.RESET_ALL}")
                    break
                except Exception as e:
                    print(Fore.RED + f"[X] Error: {str(e)}" + Style.RESET_ALL)
                    if proxy_config:
                        print_proxy_status(proxy, "Inactive")
                    print(Fore.YELLOW + "[!] Trying another proxy..." + Style.RESET_ALL)
                    break

            print(Fore.LIGHTCYAN_EX + "=" * 56 + Style.RESET_ALL)

        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled by user. Exiting...{Style.RESET_ALL}")
            break
        except Exception as e:
            print(Fore.RED + f"[X] Unexpected error: {str(e)}" + Style.RESET_ALL)
            print(Fore.LIGHTCYAN_EX + "=" * 56 + Style.RESET_ALL)

if __name__ == "__main__":
    main()