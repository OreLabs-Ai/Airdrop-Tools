

import sys
import time
import requests
import json
import os
import random
from colorama import Fore, Style
sys.dont_write_bytecode = True

class Base:
    def file_path(self, file_name):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    def create_line(self, length):
        return "═" * length

    def create_banner(self, game_name):
        return f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN}[Dev. By @nee.z.c]        {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}[Airdrop Tabizoo]           {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                     
"""

    def get_config(self, config_file, config_name):
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config.get(config_name, False)

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(f"{Fore.CYAN}{Style.BRIGHT}[{Fore.WHITE}{Style.BRIGHT}+{Fore.YELLOW}{Style.BRIGHT}]{Fore.RESET}{Fore.WHITE}{Style.BRIGHT} > {Fore.WHITE}{Style.BRIGHT}{message}")
    
    def get_random_proxy(self, proxy_file):
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip().startswith('http://')]
            return {'http': random.choice(proxies), 'https': random.choice(proxies)} if proxies else None
        except FileNotFoundError:
            self.log(f"{self.red}Error: Proxy file not found. Please create {proxy_file}")
            return None
        except Exception as e:
            self.log(f"{self.red}Error reading proxy file: {e}")
            return None

    green = "\033[92m"
    white = "\033[0m"
    yellow = "\033[93m"
    red = "\033[91m"

base = Base()

def headers(data):
    return {
        "Accept": "application/json, text/plain, /",
        "Origin": "https://miniapp.tabibot.com",
        "Rawdata": data,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

def get_info(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/profile"
    try:
        response = requests.get(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        balance = data["data"]["user"]["coins"]
        level = data["data"]["user"]["level"]
        streak = data["data"]["user"]["streak"]
        base.log(f"{base.green}Balance: {base.white}{balance:,} - {base.green}Level: {base.white}{level} - {base.green}Streak: {base.white}{streak}")
        return data
    except:
        return None

def check_in(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/check-in"
    try:
        response = requests.post(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        status = data["data"]["check_in_status"]
        return status
    except:
        return None

def process_check_in(data, proxies=None):
    check_in_status = check_in(data=data, proxies=proxies)
    if check_in_status == 1:
        base.log(f"{base.white}Auto Check-in: {base.green}Success")
    elif check_in_status == 2:
        base.log(f"{base.white}Auto Check-in: {base.red}Checked in already")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Fail")

def get_mine_project(data, proxies=None):
    url = "https://api.tabibot.com/api/task/v1/project/mine"
    try:
        response = requests.get(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        project_list = data["data"]
        return project_list
    except:
        return None

def get_project_task(data, project_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/mine?project_tag={project_tag}"
    try:
        response = requests.get(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        task_list = data["data"]["list"]
        return task_list
    except:
        return None

def do_task(data, task_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/verify/task"
    payload = {"task_tag": task_tag}
    try:
        response = requests.post(url=url, headers=headers(data=data), json=payload, proxies=proxies, timeout=20)
        data = response.json()
        status = data["data"]["verify"]
        return status
    except:
        return None

def do_project(data, project_tag, proxies=None):
    url = f"https://api.tabibot.com/api/task/v1/verify/project"
    payload = {"project_tag": project_tag}
    try:
        response = requests.post(url=url, headers=headers(data=data), json=payload, proxies=proxies, timeout=20)
        data = response.json()
        status = data["data"]["verify"]
        return status
    except:
        return None

def process_do_project_task(data, proxies=None):
    project_list = get_mine_project(data=data, proxies=proxies)
    if project_list:
        for project in project_list:
            project_tag = project["project_tag"]
            project_name = project["project_name"]
            project_status = project["user_project_status"]
            if project_status == 1:
                base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.green}Completed")
            else:
                task_list = get_project_task(data=data, project_tag=project_tag, proxies=proxies)
                for task in task_list:
                    task_tag = task["task_tag"]
                    task_name = task["task_name"]
                    task_status = task["user_task_status"]
                    if task_status == 1:
                        base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed")
                    else:
                        do_task_status = do_task(data=data, task_tag=task_tag, proxies=proxies)
                        if do_task_status:
                            base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed")
                        else:
                            base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.red}Incomplete")
                
                do_project_status = do_project(data=data, project_tag=project_tag, proxies=proxies)
                if do_project_status:
                    base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.green}Completed")
                else:
                    base.log(f"{base.white}Project: {base.yellow}{project_name} - {base.white}Status: {base.red}Incomplete")
    else:
        base.log(f"{base.white}Auto Task: {base.red}Get project list error")

def get_normal_task(data, proxies=None):
    url = "https://api.tabibot.com/api/task/v1/list"
    try:
        response = requests.get(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        project_list = data["data"]
        return project_list
    except:
        return None

def process_do_normal_task(data, proxies=None):
    project_list = get_normal_task(data=data, proxies=proxies)
    if project_list:
        for project in project_list:
            task_list = project["task_list"]
            for task in task_list:
                task_tag = task["task_tag"]
                task_name = task["task_name"]
                task_status = task["user_task_status"]
                if task_status == 1:
                    base.log(f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed")
                else:
                    do_task_status = do_task(data=data, task_tag=task_tag, proxies=proxies)
                    if do_task_status:
                        base.log(f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.green}Completed")
                    else:
                        base.log(f"{base.white}Task: {base.yellow}{task_name} - {base.white}Status: {base.red}Incomplete")
    else:
        base.log(f"{base.white}Auto Task: {base.red}Get project list error")

def get_mining_info(data, proxies=None):
    url = "https://api.tabibot.com/api/mining/v1/info"
    try:
        response = requests.get(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        rate = data["data"]["mining_data"]["rate"]
        referral_rate = data["data"]["mining_data"]["referral_rate"]
        top_limit = data["data"]["mining_data"]["top_limit"]
        current = data["data"]["mining_data"]["current"]
        base.log(f"{base.green}Mining Rate: {base.white}{rate:,} - {base.green}Refferal Bonus: {base.white}{referral_rate:,} - {base.green}Limit: {base.white}{top_limit:,} - {base.green}Mined: {base.white}{current:,}")
        return data
    except:
        return None

def claim(data, proxies=None):
    url = "https://api.tabibot.com/api/mining/v1/claim"
    try:
        response = requests.post(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        status = data["data"]
        return status
    except:
        return None

def process_claim(data, proxies=None):
    get_mining_info(data=data, proxies=proxies)
    claim_status = claim(data=data, proxies=proxies)
    if claim_status:
        base.log(f"{base.white}Auto Claim: {base.green}Success")
        get_info(data=data, proxies=proxies)
    else:
        base.log(f"{base.white}Auto Claim: {base.red}Not time to claim yet")

def upgrade(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/level-up"
    try:
        response = requests.post(url=url, headers=headers(data=data), proxies=proxies, timeout=20)
        data = response.json()
        status = data["code"]
        return status
    except:
        return None

def process_upgrade(data, proxies=None):
    upgrade_status = upgrade(data=data, proxies=proxies)
    if upgrade_status == 200:
        base.log(f"{base.white}Auto Upgrade: {base.green}Success")
        get_info(data=data, proxies=proxies)
    elif upgrade_status == 400:
        base.log(f"{base.white}Auto Upgrade: {base.red}Not enough coin")
    else:
        base.log(f"{base.white}Auto Check-in: {base.red}Unknown status")

class TabiZoo:
    def __init__(self):
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        self.proxy_file = base.file_path(file_name="proxies.txt")
        self.line = base.create_line(length=50)
        self.banner = base.create_banner(game_name="TabiZoo")
        self.auto_check_in = base.get_config(config_file=self.config_file, config_name="auto-check-in")
        self.auto_do_task = base.get_config(config_file=self.config_file, config_name="auto-do-task")
        self.auto_claim = base.get_config(config_file=self.config_file, config_name="auto-claim")
        self.auto_upgrade = base.get_config(config_file=self.config_file, config_name="auto-upgrade")

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            data = open(self.data_file, "r").read().splitlines()
            num_acc = len(data)
            base.log(self.line)
            base.log(f"{base.green}Number of accounts: {base.white}{num_acc}")

            for no, data in enumerate(data):
                base.log(self.line)
                base.log(f"{base.green}Account number: {base.white}{no+1}/{num_acc}")

                try:
                    proxies = base.get_random_proxy(self.proxy_file)
                    if proxies:
                        base.log(f"{base.yellow}Proxy: {base.green}ON")
                    else:
                        base.log(f"{base.yellow}Proxy: {base.red}OFF (No valid proxies found)")

                    get_info(data=data, proxies=proxies)

                    if self.auto_check_in:
                        base.log(f"{base.yellow}Auto Check-in: {base.green}ON")
                        process_check_in(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Check-in: {base.red}OFF")

                    if self.auto_do_task:
                        base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                        process_do_project_task(data=data, proxies=proxies)
                        process_do_normal_task(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                    if self.auto_claim:
                        base.log(f"{base.yellow}Auto Claim: {base.green}ON")
                        process_claim(data=data)
                    else:
                        base.log(f"{base.yellow}Auto Claim: {base.red}OFF")

                    if self.auto_upgrade:
                        base.log(f"{base.yellow}Auto Upgrade: {base.green}ON")
                        process_upgrade(data=data)
                    else:
                        base.log(f"{base.yellow}Auto Upgrade: {base.red}OFF")

                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        tabi = TabiZoo()
        tabi.main()
    except KeyboardInterrupt:
        sys.exit()