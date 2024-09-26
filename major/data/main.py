import os
import json
import time
from datetime import datetime
from colorama import Fore, Style


last_log_message = None

def _banner():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN}[Dev. By @nee.z.c]        {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}[Airdrop MAJOR🌟]           {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""
    print(banner)  # Tambahkan ini agar banner tampil
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(config_path, 'r') as file:
        try:
            config_content = file.read()
            return json.loads(config_content)
        except json.JSONDecodeError as e:
            return {}
        
def log(message, **kwargs):
    global last_log_message
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    flush = kwargs.pop('flush', False)
    end = kwargs.pop('end', '\n')
    if message != last_log_message:
        print(f"{Fore.BLACK} {Style.BRIGHT}[#] {message}", flush=flush, end=end)
        last_log_message = message

def log_line():
    print(Fore.WHITE + "━" * 50)

def countdown_timer(seconds):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"{Fore.WHITE}please wait until {h}:{m}:{s} ", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"{Fore.WHITE}please wait until {h}:{m}:{s} ", flush=True, end="\r")

def _number(number):
    return "{:,.0f}".format(number)