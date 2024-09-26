import sys
import time
import requests
from colorama import Fore, Style

sys.dont_write_bytecode = True

class Base:
    def __init__(self):
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.white = '\033[0m'

    def log(self, message):
        print(f"{Fore.CYAN}{Style.BRIGHT}[{Fore.WHITE}{Style.BRIGHT}+{Fore.YELLOW}{Style.BRIGHT}]{Fore.RESET}{Fore.WHITE}{Style.BRIGHT} > {Fore.WHITE}{Style.BRIGHT}{message}")

    def clear_terminal(self):
        print('\033c', end='')

    def create_line(self, length=50):
        return '═' * length

    def create_banner(self, game_name):
        banner = f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN} Dev. By @nee.z.c         {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}Airdrop Cyber Finance       {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    """
        return banner

    def file_path(self, file_name):
        return file_name

    def get_config(self, config_file, config_name):
        # Simplified config reading (you may want to implement proper JSON parsing)
        return True

base = Base()

def headers(token=None):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://g.cyberfin.xyz",
        "Referer": "https://g.cyberfin.xyz/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def get_token(data, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/game/initdata"
    payload = {"initData": data}

    try:
        response = requests.post(
            url=url, headers=headers(), json=payload, proxies=proxies, timeout=20
        )
        data = response.json()
        token = data["message"]["accessToken"]
        return token
    except:
        return None

def game_data(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/game/mining/gamedata"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        balance = data["message"]["userData"]["balance"]
        balance = int(float(balance))
        return balance
    except:
        return None

def get_task(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/gametask/all"
    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        task_list = data["message"]
        return task_list
    except:
        return None

def get_ads(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/ads/count"
    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        ads_count = data["message"]["amountLeftToView"]
        return ads_count
    except:
        return None

def do_task(token, task_id, proxies=None):
    url = f"https://api.cyberfin.xyz/api/v1/gametask/complete/{task_id}"
    try:
        response = requests.patch(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None

def watch_ads(token, proxies=None):
    url = f"https://api.cyberfin.xyz/api/v1/ads/log"
    try:
        response = requests.post(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None

def process_do_task(token, proxies=None):
    task_list = get_task(token=token, proxies=proxies)
    if task_list:
        for task in task_list:
            task_id = task["uuid"]
            task_name = task["title"]
            is_completed = task["isCompleted"]
            is_active = task["isActive"]
            if is_completed:
                base.log(f"{base.white}{task_name}: {base.green}Completed")
            else:
                if is_active:
                    start_do_task = do_task(
                        token=token, task_id=task_id, proxies=proxies
                    )
                    try:
                        status = start_do_task["code"]
                        if status == 200:
                            base.log(f"{base.white}{task_name}: {base.green}Completed")
                        else:
                            base.log(f"{base.white}{task_name}: {base.red}Incomplete")
                    except:
                        base.log(f"{base.white}{task_name}: {base.red}Incomplete")
                else:
                    base.log(f"{base.white}{task_name}: {base.red}Inactive")
    else:
        base.log(f"{base.white}Auto Do Task: {base.red}Get task list error")

def process_watch_ads(token, proxies=None):
    while True:
        ads_count = get_ads(token=token, proxies=proxies)
        if ads_count > 0:
            start_watch_ads = watch_ads(token=token, proxies=proxies)
            try:
                value = start_watch_ads["message"]["value"]
                base.log(
                    f"{base.white}Auto Watch Ads: {base.green}Success | Added {value:,} points"
                )
            except:
                base.log(f"{base.white}Auto Watch Ads: {base.red}Watch ads error")
                break
        else:
            base.log(f"{base.white}Auto Watch Ads: {base.red}No ads to watch")
            break

def claim(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/claim"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        return data
    except:
        return None

def process_claim(token, proxies=None):
    start_claim = claim(token=token, proxies=proxies)
    try:
        balance = start_claim["message"]["userData"]["balance"]
        balance = int(float(balance))
        base.log(
            f"{base.white}Auto Claim: {base.green}Success {base.white}| {base.green}New balance: {base.white}{balance:,}"
        )
    except:
        base.log(f"{base.white}Auto Claim: {base.red}Not time to claim")

def boost(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/boost/info"

    try:
        response = requests.get(
            url=url, headers=headers(token=token), proxies=proxies, timeout=20
        )
        data = response.json()
        hammer_price = data["message"]["hammerPrice"]
        return hammer_price
    except:
        return None

def buy_boost(token, proxies=None):
    url = "https://api.cyberfin.xyz/api/v1/mining/boost/apply"
    payload = {"boostType": "HAMMER"}

    try:
        response = requests.post(
            url=url,
            headers=headers(token=token),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        status = data["code"]
        return status
    except:
        return None

def process_buy_boost(token, limit_price, proxies=None):
    while True:
        hammer_price = boost(token=token, proxies=proxies)
        if hammer_price < limit_price:
            base.log(
                f"{base.white}Auto Buy Hammer: {base.green}Start buying boost {base.white}| {base.yellow}Hammer Price: {base.white}{hammer_price:,} - {base.yellow}Limit Price: {base.white}{limit_price:,}"
            )
            buy_boost_status = buy_boost(token=token, proxies=proxies)
            if buy_boost_status == 200:
                base.log(f"{base.white}Auto Buy Hammer: {base.green}Success")
            else:
                base.log(
                    f"{base.white}Auto Buy Hammer: {base.red}Re-check your balance"
                )
                break
        else:
            base.log(
                f"{base.white}Auto Buy Hammer: {base.red}Limit reached. Stop! {base.white}| {base.yellow}Hammer Price: {base.white}{hammer_price:,} - {base.yellow}Limit Price: {base.white}{limit_price:,}"
            )
            break

class CyberFinance:
    def __init__(self):
        self.data_file = base.file_path(file_name="data.txt")
        self.config_file = base.file_path(file_name="config.json")
        self.line = base.create_line(length=50)
        self.banner = base.create_banner(game_name="Cyber Finance")
        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )
        self.auto_watch_ads = base.get_config(
            config_file=self.config_file, config_name="auto-watch-ads"
        )
        self.auto_claim = base.get_config(
            config_file=self.config_file, config_name="auto-claim"
        )
        self.auto_buy_hammer = base.get_config(
            config_file=self.config_file, config_name="auto-buy-hammer"
        )

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
                    token = get_token(data=data)

                    if token:
                        balance = game_data(token=token)
                        base.log(f"{base.green}Balance: {base.white}{balance:,}")

                        if self.auto_do_task:
                            base.log(f"{base.yellow}Auto Do Task: {base.green}ON")
                            process_do_task(token=token)
                        else:
                            base.log(f"{base.yellow}Auto Do Task: {base.red}OFF")

                        if self.auto_watch_ads:
                            base.log(f"{base.yellow}Auto Watch Ads: {base.green}ON")
                            process_watch_ads(token=token)
                        else:
                            base.log(f"{base.yellow}Auto Watch Ads: {base.red}OFF")

                        if self.auto_claim:
                            base.log(f"{base.yellow}Auto Claim: {base.green}ON")
                            process_claim(token=token)
                        else:
                            base.log(f"{base.yellow}Auto Claim: {base.red}OFF")

                        if self.auto_buy_hammer:
                            base.log(f"{base.yellow}Auto Buy Hammer: {base.green}ON")
                            hammer_limit_price = 10000
                            process_buy_boost(
                                token=token, limit_price=hammer_limit_price
                            )
                        else:
                            base.log(f"{base.yellow}Auto Buy Hammer: {base.red}OFF")

                        balance = game_data(token=token)
                        base.log(f"{base.green}Balance: {base.white}{balance:,}")
                    else:
                        base.log(f"{base.red}Token not found! Please get new query id")
                except Exception as e:
                    base.log(f"{base.red}Error: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}Wait for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)

if __name__ == "__main__":
    try:
        cyberfinance = CyberFinance()
        cyberfinance.main()
    except KeyboardInterrupt:
        sys.exit()