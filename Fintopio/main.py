import os
import time
import sys
import re
import json
import requests
from urllib.parse import unquote
from pyfiglet import Figlet
from colorama import Fore, Style, init
import random

init(autoreset=True)  # Initialize colorama

api = "https://fintopio-tg.fintopio.com/api"
header = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://fintopio-tg.fintopio.com/",
    "Sec-Ch-Ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Webapp": "true"
}

use_proxy = False
account_proxies = {}
user_data = {}
telegram_chat_id = None  # To hold the Telegram chat ID
bot_token = "7082817649:AAFi2caK7jcm_fc8irZqcDwsG7dCTJ-GEks"  # Your Telegram Bot Token

def load_proxies():
    with open('proxies.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

proxies = load_proxies()

def send_log_to_telegram(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        custom_log(f'Error sending message to Telegram: {str(e)}', Fore.RED, "TELEGRAM")

def get_proxy_for_account(account):
    if account not in account_proxies:
        account_proxies[account] = random.choice(proxies) if proxies else None
    return account_proxies[account]

def create_session_with_proxy(account):
    s = requests.Session()
    if use_proxy:
        proxy = get_proxy_for_account(account)
        if proxy:
            s.proxies = {'http': proxy, 'https': proxy}
            custom_log(f"Proxy Active [✓] : ", Fore.CYAN)
        else:
            custom_log(f"No proxy available. Running without proxy.", Fore.YELLOW)
    else:
        custom_log(f"Running without Proxy !!", Fore.YELLOW)
    s.headers.update({"Webapp": "true"})
    return s

def banner():
    os.system("title FINTOPIO BOT" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")
    
    nez_fin_banner = f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN}[Dev. By @nee.z.c]        {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}[Airdrop Fintopio]          {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
    """ + Style.RESET_ALL
    print(nez_fin_banner)

def custom_log(message, color=Fore.WHITE, log_type="INFO"):
    print(f"{color}{Style.BRIGHT}[+] [{log_type}] {message}{Style.RESET_ALL}")
    send_log_to_telegram(message)  # Send log to Telegram

def runforeva(): 
    with open('data.txt', 'r') as file:
        queryh = file.read().splitlines()
    try:
        value = True
        while value:
            for index, query_id in enumerate(queryh, start=1):
                account = f"Account_{index}"
                username = getname(query_id, account)
                if username:
                    token = getlogin(query_id, account)
                    if token:
                        postrequest(token, account)
    except Exception as e:
        custom_log(f'Error in main loop: {str(e)}', Fore.RED, "MAIN")
        time.sleep(5)
        runforeva()

def getlogin(querybro, account):
    try:
        url = api + "/auth/telegram?"
        s = create_session_with_proxy(account)
        response = s.get(url + querybro, headers=header)
        jData = response.json()
        jsontoken = jData['token']
        custom_log(f'Login success for @{user_data[account]["username"]}', Fore.GREEN, "SUCCESS")
        return jsontoken
    except Exception as e:
        custom_log(f'Login error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "LOGIN")
        return None

def getname(querybro, account):
    try:
        found = re.search('user=([^&]*)', querybro).group(1)
        decodedUserPart = unquote(found)
        userObj = json.loads(decodedUserPart)
        user_data[account] = userObj
        custom_log(f"Username for @{userObj['username']}: @{userObj['username']}", Fore.GREEN, "SUCCESS")
        return userObj['username']
    except Exception as e:
        custom_log(f'Error getting username: {str(e)}', Fore.RED, "USERNAME")
        return None

def checkin(token, account):
    try:
        url = api + "/daily-checkins"
        s = create_session_with_proxy(account)
        s.headers.update({"Authorization": "Bearer " + token})
        response = s.post(url, headers=header)
        jData = response.json()
        custom_log(f"Reward daily for @{user_data[account]['username']}: {jData['dailyReward']}", Fore.YELLOW, "REWARD")
        custom_log(f"Total login days for @{user_data[account]['username']}: {jData['totalDays']}", Fore.YELLOW, "TOTAL")
        custom_log(f'Daily reward claimed for @{user_data[account]["username"]}!', Fore.GREEN, "SUCCESS")
    except Exception as e:
        custom_log(f'Checkin failed for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "CHECKIN")

def nuke(token, id, reward, account):
    try:
        url = api + "/clicker/diamond/complete"
        s = create_session_with_proxy(account)
        s.headers.update({"Authorization": "Bearer " + token})
        textpayload = {"diamondNumber": id}
        response = s.post(url, headers=header, json=textpayload)
        if response.status_code != 200:
            custom_log(f'Failed to claim for @{user_data[account]["username"]}', Fore.RED, "ASTEROID")
        else:
            custom_log(f'Asteroid was crushed for @{user_data[account]["username"]}!', Fore.GREEN, "SUCCESS")
            custom_log(f"Reward for @{user_data[account]['username']}: {reward}", Fore.YELLOW, "REWARD")
    except Exception as e:
        custom_log(f'Asteroid error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "ASTEROID")

def tanamtanamubi(token, account):
    try:
        url = api + "/farming/farm"
        s = create_session_with_proxy(account)
        s.headers.update({"Authorization": "Bearer " + token})
        response = s.post(url, headers=header)
        if response.status_code != 200:
            custom_log(f'Failed to start farming for @{user_data[account]["username"]}', Fore.RED, "FARMING")
        else:
            custom_log(f'Farming started for @{user_data[account]["username"]}!', Fore.GREEN, "SUCCESS")
    except Exception as e:
        custom_log(f'Farming start error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "FARMING")

def panenbrow(token, account):
    try:
        url = api + "/farming/claim"
        s = create_session_with_proxy(account)
        s.headers.update({"Authorization": "Bearer " + token})
        response = s.post(url, headers=header)
        if response.status_code == 200:
            custom_log(f'Farming claimed for @{user_data[account]["username"]}!', Fore.GREEN, "SUCCESS")
        else:
            custom_log(f'Failed to claim farming for @{user_data[account]["username"]}', Fore.RED, "FARMING")
    except Exception as e:
        custom_log(f'Farming claim error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "FARMING")

def gettask(token, account):
    try:
        urltasks = api + "/hold/tasks"
        s = create_session_with_proxy(account)
        s.headers.update({"Authorization": "Bearer " + token})
        response = s.get(urltasks, headers=header)
        jData = response.json()
        jTask = jData['tasks']

        for item in jTask: 
            if item['status'] == 'available':
                urlstart = f"/hold/tasks/{item['id']}/start"
                s.post(api+urlstart, headers=header)
                custom_log(f"Task {item['slug']} started for @{user_data[account]['username']}!", Fore.YELLOW, "TASK")
            elif item['status'] == 'verified':
                urlclaim = f"/hold/tasks/{item['id']}/claim"
                responseclaim = s.post(api+urlclaim, headers=header)
                if responseclaim.json().get('status') == 'completed':
                    custom_log(f"Task {item['slug']} claimed {item['rewardAmount']} points for @{user_data[account]['username']}", Fore.GREEN, "SUCCESS")
    except Exception as e:
        custom_log(f'Task error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "TASK")

def sleep(num):
    for i in range(num):
        print(f"{Fore.CYAN}{Style.BRIGHT}[+] wait {num - i} seconds{Style.RESET_ALL}", end='\r')
        time.sleep(1)

def postrequest(token, account):
    urldata = '/referrals/data'
    urldiamondstate = '/clicker/diamond/state'
    urlfarmstate = '/farming/state'

    s = create_session_with_proxy(account)
    s.headers.update({"Authorization": "Bearer " + token})

    try:
        r = s.get(api+urldata, headers=header)
        jData = r.json()
        if not jData['isDailyRewardClaimed']:
            custom_log(f'Daily reward not claimed yet for @{user_data[account]["username"]}', Fore.YELLOW, "DAILY")
            custom_log(f'Claiming for @{user_data[account]["username"]}..', Fore.YELLOW, "DAILY")
            checkin(token, account)
        custom_log(f"Balance for @{user_data[account]['username']}: {jData['balance']}", Fore.YELLOW, "BALANCE")
        gettask(token, account)
    except Exception as e:
        custom_log(f'Data error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "DAILY")

    try:
        r2 = s.get(api+urldiamondstate, headers=header)
        jData = r2.json()
        if jData['state'] == 'available':
            nuke(token, jData['diamondNumber'], jData['settings']['totalReward'], account)
        elif jData['state'] == 'unavailable':
            custom_log(f'Asteroid unavailable yet for @{user_data[account]["username"]}!', Fore.YELLOW, "ASTEROID")
        else:
            custom_log(f'Asteroid crushed for @{user_data[account]["username"]}! Waiting next round..', Fore.YELLOW, "ASTEROID")
    except Exception as e:
        custom_log(f'Asteroid state error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "ASTEROID")

    try:
        r3 = s.get(api+urlfarmstate, headers=header)
        jData = r3.json()
        if jData['state'] == 'idling':
            tanamtanamubi(token, account)
        elif jData['state'] == 'farming':
            custom_log(f'Farming not finished yet for @{user_data[account]["username"]}!', Fore.YELLOW, "FARMING")
        elif jData['state'] == 'farmed':
            panenbrow(token, account)
        else:
            custom_log(f'Unknown farming state for @{user_data[account]["username"]}', Fore.RED, "FARMING")
        print(f"{Fore.CYAN}{Style.BRIGHT}[+] ========================================={Style.RESET_ALL}")
        sleep(3)
    except Exception as e:
        custom_log(f'Farming state error for @{user_data[account]["username"]}: {str(e)}', Fore.RED, "FARMING")

if __name__ == "__main__":
    try:
        banner()  # Display banner

        # Ask for Telegram Chat ID for log notifications (with red and bold text)
        telegram_chat_id = input("\033[31m\033[1mEnter your Telegram chat ID for log notifications: \033[0m")
        
        # Ask whether to use a proxy
        proxy_choice = input("Do you want to use a proxy? (Y/N): ").strip().upper()
        use_proxy = proxy_choice == 'Y'
        
        # Start the process
        custom_log("Starting bot...", Fore.CYAN, "INIT")
        runforeva()  # Run the bot loop
    except KeyboardInterrupt:
        custom_log("Bot stopped by user.", Fore.YELLOW, "STOP")
    except Exception as e:
        custom_log(f"Unexpected error: {str(e)}", Fore.RED, "ERROR")