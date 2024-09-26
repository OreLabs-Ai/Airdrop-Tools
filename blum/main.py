import os
import re
import sys
import json
import anyio
import httpx
import telebot
import random
import asyncio
import argparse
import aiofiles
import aiofiles.os
from base64 import b64decode
import aiofiles.ospath
from colorama import init, Fore, Style
from urllib.parse import parse_qs
from datetime import datetime
from po.user import ( get_by_id )
from po.com import ( init as init_db )
from po.ring import ( update_token )
from po.login import ( update_balance )
from po.repo import ( insert )
from po.data import ( get_token )
import python_socks
from httpx_socks import AsyncProxyTransport
import telebot

init(autoreset=True)

red = Fore.LIGHTRED_EX
blue = Fore.BLUE
biru = Fore.LIGHTBLUE_EX
kuning = Fore.YELLOW
green = Fore.GREEN
yellow = Fore.YELLOW
black = Fore.LIGHTBLACK_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL
ungu = Fore.CYAN
tebal = Style.BRIGHT
magenta = Fore.LIGHTMAGENTA_EX
line = white + "~" * 50
log_file = "http.log"
proxy_file = "proxies.txt"
data_file = "data.txt"
config_file = "config.json"

class Config:
    def __init__(self, auto_task, auto_game, auto_claim, low, high, telegram_id):
        self.auto_task = auto_task
        self.auto_game = auto_game
        self.auto_claim = auto_claim
        self.low = low
        self.high = high
        self.telegram_id = telegram_id

class BlumAirdrop:
    def __init__(self, id, query, proxies, config: Config):
        self.p = id
        self.query = query
        self.proxies = proxies
        self.cfg = config
        self.valid = True
        parser = {key: value[0] for key, value in parse_qs(query).items()}
        user = parser.get("user")
        if user is None:
            self.valid = False
            self.log(f"{red}this account data has the wrong format.")
            return None
        uid = re.search(r'"id":(.*?),', user).group(1)
        first_name = re.search(r'first_name":"(.*?)"', user).group(1)
        self.user = {"id": uid, "first_name": first_name}
        if len(self.proxies) > 0:
            proxy = self.get_random_proxy(id, False)
            transport = AsyncProxyTransport.from_url(proxy)
            self.ses = httpx.AsyncClient(transport=transport, timeout=1000)
        else:
            self.ses = httpx.AsyncClient(timeout=1000)
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
            "content-type": "application/json",
            "origin": "https://telegram.blum.codes",
            "x-requested-with": "org.telegram.messenger",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://telegram.blum.codes/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en,en-US;q=0.9",
        }

    def log(self, msg):
        now = datetime.now().isoformat().split("T")[1].split(".")[0]
        log_message = f"{blue}{tebal}[{white}{tebal}+{yellow}]{white}-{blue}[{white}acc {self.p + 1}{blue}]{white} {msg}{reset}"
        print(log_message)
        self.send_telegram_message(log_message)

    def send_telegram_message(self, message):
        bot = telebot.TeleBot("7856924217:AAFCCas7iih5dF7vw5Aml0WQA0luwX2V2zU")
        chat_id = self.cfg.telegram_id
        

    async def ipinfo(self):
        ipinfo1_url = "https://ipapi.co/json/"
        ipinfo2_url = "https://ipwho.is/"
        ipinfo3_url = "https://freeipapi.com/api/json"
        try:
            res = await self.ses.get(ipinfo1_url)
            ip = res.json().get("ip")
            country = res.json().get("country")
            if not ip:
                res = await self.ses.get(ipinfo2_url)
                ip = res.json().get("ip")
                country = res.json().get("country_code")
                if not ip:
                    res = await self.ses.get(ipinfo3_url)
                    ip = res.json().get("ipAddress")
                    country = res.json().get("countryCode")
            self.log(f"{red}{tebal}ip : {white}{ip} {red}country : {white}{country}")
        except json.decoder.JSONDecodeError:
            self.log(f"{red}ip : {white}None {red}country : {white}None")

    def get_random_proxy(self, isself, israndom=False):
        if israndom:
            return random.choice(self.proxies)
        return self.proxies[isself % len(self.proxies)]

    async def http(self, url, headers, data=None):
        while True:
            try:
                if not await aiofiles.ospath.exists(log_file):
                    async with aiofiles.open(log_file, "w") as w:
                        await w.write("")
                logsize = await aiofiles.ospath.getsize(log_file)
                if logsize / 1024 / 1024 > 1:
                    async with aiofiles.open(log_file, "w") as w:
                        await w.write("")
                if data is None:
                    res = await self.ses.get(url, headers=headers)
                elif data == "":
                    res = await self.ses.post(url, headers=headers)
                else:
                    res = await self.ses.post(url, headers=headers, data=data)
                async with aiofiles.open(log_file, "a", encoding="utf-8") as hw:
                    await hw.write(f"{res.status_code} {res.text}\n")
                if "<title>" in res.text:
                    self.log(f"{yellow}{tebal}Server Down  !")
                    await countdown(3)
                    continue

                return res
            except (httpx.ProxyError, python_socks._errors.ProxyTimeoutError):
                proxy = self.get_random_proxy(0, israndom=True)
                transport = AsyncProxyTransport.from_url(proxy)
                self.ses = httpx.AsyncClient(transport=transport)
                self.log(f"{yellow}proxy error,selecting random proxy !")
                await asyncio.sleep(3)
                continue
            except httpx.NetworkError:
                self.log(f"{yellow}network error !")
                await asyncio.sleep(3)
                continue
            except httpx.TimeoutException:
                self.log(f"{yellow}connection timeout !")
                await asyncio.sleep(3)
                continue
            except (httpx.RemoteProtocolError, anyio.EndOfStream):
                self.log(f"{yellow}connection close without response !")
                await asyncio.sleep(3)
                continue

    def is_expired(self, token):
        if token is None or isinstance(token, bool):
            return True
        header, payload, sign = token.split(".")
        payload = b64decode(payload + "==").decode()
        jload = json.loads(payload)
        now = round(datetime.now().timestamp()) + 300
        exp = jload["exp"]
        if now > exp:
            return True

        return False

    async def login(self):
        auth_url = "https://user-domain.blum.codes/api/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP"
        data = {
            "query": self.query,
        }
        res = await self.http(auth_url, self.headers, json.dumps(data))
        token = res.json().get("token")
        if not token:
            self.log(f"{red}{tebal}failed get access token !")
            return 3600
        token = token.get("access")
        uid = self.user.get("id")
        await update_token(uid, token)
        self.log(f"{green}{tebal}success get access token !")
        self.headers["authorization"] = f"Bearer {token}"

    async def start(self):
        if not self.valid:
            return int(datetime.now().timestamp()) + (3600 * 8)
        balance_url = "https://game-domain.blum.codes/api/v1/user/balance"
        friend_balance_url = "https://user-domain.blum.codes/api/v1/friends/balance"
        farming_claim_url = "https://game-domain.blum.codes/api/v1/farming/claim"
        farming_start_url = "https://game-domain.blum.codes/api/v1/farming/start"
        checkin_url = "https://game-domain.blum.codes/api/v1/daily-reward?offset=-420"
        if len(self.proxies) > 0:
            await self.ipinfo()
        uid = self.user.get("id")
        first_name = self.user.get("first_name")
        self.log(f"{biru}login as {white}{first_name}")
        avail = await get_by_id(uid)
        if not avail:
            await insert(uid, first_name)
        token = await get_token(uid)
        expired = self.is_expired(token=token)
        if expired:
            await self.login()
        else:
            self.headers["authorization"] = f"Bearer {token}"
        res = await self.http(checkin_url, self.headers)
        if res.status_code == 404:
            self.log(f"{yellow}{tebal}already check in today !")
        else:
            res = await self.http(checkin_url, self.headers, "")
            self.log(f"{green}{tebal}success check in today !")
        while True:
            res = await self.http(balance_url, self.headers)
            timestamp = res.json().get("timestamp")
            if timestamp == 0:
                timestamp = int(datetime.now().timestamp() * 1000)
            if not timestamp:
                continue
            timestamp = timestamp / 1000
            break
        balance = res.json().get("availableBalance", 0)
        await update_balance(uid, balance)
        farming = res.json().get("farming")
        end_iso = datetime.now().isoformat(" ")
        end_farming = int(datetime.now().timestamp() * 1000) + random.randint(
            3600000, 7200000
        )
        self.log(f"{biru}{tebal}balance : {white}{balance}")
        refres = await self.http(friend_balance_url, self.headers)
        amount_claim = refres.json().get("amountForClaim")
        can_claim = refres.json().get("canClaim", False)
        self.log(f"{green}{tebal}referral balance : {white}{amount_claim}")
        if can_claim:
            friend_claim_url = "https://user-domain.blum.codes/api/v1/friends/claim"
            clres = await self.http(friend_claim_url, self.headers, "")
            if clres.json().get("claimBalance") is not None:
                self.log(f"{green}success claim referral reward !")
            else:
                self.log(f"{red}failed claim referral reward !")
        if self.cfg.auto_claim:
            while True:
                if farming is None:
                    _res = await self.http(farming_start_url, self.headers, "")
                    if _res.status_code != 200:
                        self.log(f"{red}{tebal}failed start farming !")
                    else:
                        self.log(f"{ungu}{tebal}success start farming !")
                        farming = _res.json()
                if farming is None:
                    res = await self.http(balance_url, self.headers)
                    farming = res.json().get("farming")
                    if farming is None:
                        continue
                end_farming = farming.get("endTime")
                if timestamp > (end_farming / 1000):
                    res_ = await self.http(farming_claim_url, self.headers, "")
                    if res_.status_code != 200:
                        self.log(f"{red}failed claim farming !")
                    else:
                        self.log(f"{green}success claim farming !")
                        farming = None
                        continue
                else:
                    self.log(f"{yellow}{tebal}wait for the next claim  !")
                end_iso = (
                    datetime.fromtimestamp(end_farming / 1000)
                    .isoformat(" ")
                    .split(".")[0]
                )
                break
            self.log(f"{kuning}{tebal}Last Farming : {white}{end_iso}")
        if self.cfg.auto_task:
            task_url = "https://earn-domain.blum.codes/api/v1/tasks"
            res = await self.http(task_url, self.headers)
            for tasks in res.json():
                if isinstance(tasks, str):
                    self.log(f"{yellow}failed get task list !")
                    break
                for k in list(tasks.keys()):
                    if k != "tasks" and k != "subSections":
                        continue
                    for t in tasks.get(k):
                        if isinstance(t, dict):
                            subtasks = t.get("subTasks")
                            if subtasks is not None:
                                for task in subtasks:
                                    await self.solve(task)
                                await self.solve(t)
                                continue
                        _tasks = t.get("tasks")
                        if not _tasks:
                            continue
                        for task in _tasks:
                            await self.solve(task)
        if self.cfg.auto_game:
            play_url = "https://game-domain.blum.codes/api/v1/game/play"
            claim_url = "https://game-domain.blum.codes/api/v1/game/claim"
            while True:
                res = await self.http(balance_url, self.headers)
                play = res.json().get("playPasses")
                if play is None:
                    self.log(f"{yellow}{tebal}failed get game ticket !")
                    break
                self.log(f"{red}{tebal}you have {white}{play}{red}{tebal} game ticket")
                if play <= 0:
                    break
                for i in range(play):
                    if self.is_expired(self.headers.get("authorization").split(" ")[1]):
                        await self.login()
                        continue
                    res = await self.http(play_url, self.headers, "")
                    game_id = res.json().get("gameId")
                    if game_id is None:
                        message = res.json().get("message", "")
                        if message == "cannot start game":
                            self.log(f"{yellow}{message}")
                            break
                        self.log(f"{yellow}{message}")
                        continue
                    while True:
                        await countdown(30)
                        point = random.randint(self.cfg.low, self.cfg.high)
                        data = json.dumps({"gameId": game_id, "points": point})
                        res = await self.http(claim_url, self.headers, data)
                        if "OK" in res.text:
                            self.log(
                                f"{ungu}{tebal}success earn {white}{point}{ungu} {tebal}from game !"
                            )
                            break
                        message = res.json().get("message", "")
                        if message == "game session not finished":
                            continue
                        self.log(f"{red}failed earn {white}{point}{red} from game !")
                        break
        res = await self.http(balance_url, self.headers)
        balance = res.json().get("availableBalance", 0)
        self.log(f"{green}balance :{white}{balance}")
        await update_balance(uid, balance)
        return round(end_farming / 1000)

    async def solve(self, task: dict):
        task_id = task.get("id")
        task_title = task.get("title")
        task_status = task.get("status")
        task_type = task.get("type")
        validation_type = task.get("validationType")
        start_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/start"
        claim_task_url = f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/claim"
        while True:
            if task_status == "FINISHED":
                self.log(f"{ungu}Checking Taskk..... 🐝{white} !")
                return
            if task_status == "READY_FOR_CLAIM" or task_status == "STARTED":
                _res = await self.http(claim_task_url, self.headers, "")
                message = _res.json().get("message")
                if message:
                    return
                _status = _res.json().get("status")
                if _status == "FINISHED":
                    self.log(f"{magenta}Task Complete!!🌟 {white} !")
                    return
            if task_status == "NOT_STARTED" and task_type == "PROGRESS_TARGET":
                return
            if task_status == "NOT_STARTED":
                _res = await self.http(start_task_url, self.headers, "")
                await countdown(3)
                message = _res.json().get("message")
                if message:
                    return
                task_status = _res.json().get("status")
                continue
            if validation_type == "KEYWORD" or task_status == "READY_FOR_VERIFY":
                verify_url = (
                    f"https://earn-domain.blum.codes/api/v1/tasks/{task_id}/validate"
                )
                answer_url = "https://akasakaid.github.io/blum/answer.json"
                res_ = await self.http(answer_url, {"User-Agent": "Marin Kitagawa"})
                answers = res_.json()
                answer = answers.get(task_id)
                if not answer:
                    self.log(f"{magenta}Waiting for the next Quiz .... ^^ ")
                    return
                data = {"keyword": answer}
                res = await self.http(verify_url, self.headers, json.dumps(data))
                message = res.json().get("message")
                if message:
                    return
                task_status = res.json().get("status")
                continue


async def countdown(t):
    for i in range(t, 0, -1):
        minute, seconds = divmod(i, 60)
        hour, minute = divmod(minute, 60)
        seconds = str(seconds).zfill(2)
        minute = str(minute).zfill(2)
        hour = str(hour).zfill(2)
        print(f"{yellow}{tebal}waiting for {hour}:{minute}:{seconds} ", flush=True, end="\r")
        await asyncio.sleep(1)


async def get_data(data_file, proxy_file):
    async with aiofiles.open(data_file) as w:
        read = await w.read()
        datas = [i for i in read.splitlines() if len(i) > 10]
    async with aiofiles.open(proxy_file) as w:
        read = await w.read()
        proxies = [i for i in read.splitlines() if len(i) > 5]
    return datas, proxies

async def main():
    banner = f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══��═══╝ �������═══╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━��━━━━━━���━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN}[Dev. By @nee.z.c]        {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}[Airdrop Blum    ]          {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    arg = argparse.ArgumentParser()
    arg.add_argument("--data", "-D", default=data_file, help=f"Perform custom input for data files (default: {data_file})")
    arg.add_argument("--proxy", "-P", default=proxy_file, help=f"Perform custom input for proxy files (default : {proxy_file})")
    arg.add_argument("--action", "-A", help="Function to directly enter the menu without displaying input")
    arg.add_argument("--worker", "-W", help="Total workers or number of threads to be used (default : cpu core / 2)")
    arg.add_argument("--marin", action="store_true")
    args = arg.parse_args()

    if not await aiofiles.ospath.exists(args.data):
        async with aiofiles.open(args.data, "a") as w:
            pass
    if not await aiofiles.ospath.exists(args.proxy):
        async with aiofiles.open(args.proxy, "a") as w:
            pass
    if not await aiofiles.ospath.exists(config_file):
        async with aiofiles.open(config_file, "w") as w:
            _config = {
                "auto_claim": True,
                "auto_task": True,
                "auto_game": True,
                "low": 240,
                "high": 250,
                "telegram_id": ""
            }
            await w.write(json.dumps(_config, indent=4))

    while True:
        if not args.marin:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)

        async with aiofiles.open(config_file) as r:
            read = await r.read()
            cfg = json.loads(read)

        print(f"[{green}+{white}] Input your Telegram ID: ", end="")
        telegram_id = input()
        cfg["telegram_id"] = telegram_id

        config = Config(
            auto_task=cfg.get("auto_task"),
            auto_game=cfg.get("auto_game"),
            auto_claim=cfg.get("auto_claim"),
            low=int(cfg.get("low", 240)),
            high=int(cfg.get("high", 250)),
            telegram_id=cfg.get("telegram_id")
        )

        datas, proxies = await get_data(data_file=args.data, proxy_file=args.proxy)

        
        print(f"{red}{tebal}Total data: {white}{len(datas)}")
        print(f"{red}{tebal}Total proxy: {white}{len(proxies)}\n")

        # Auto claim mode
        print(f"{ungu}{tebal}[{green}+{white}] Auto Claim Mode: {green}{config.auto_claim}{white}")
        auto_claim = input(f"  {yellow}Enter True/False to change (or press Enter to skip): ").lower()

        if (auto_claim == 'true' and not config.auto_claim) or (auto_claim == 'false' and config.auto_claim):
            cfg["auto_claim"] = (auto_claim == 'true')
            print(f"{green}Auto claim config updated successfully!")
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(cfg, indent=4))
            print(f"\n{red}Auto claim configuration has been reset based on your input.")
            input(f"\n{blue}Press Enter to continue...")
            return await main()

        # Auto task mode
        print(f"{ungu}{tebal}[{green}+{white}] Auto Task: {green}{config.auto_task}{white}")
        auto_task = input(f" {yellow}  Enter True/False to change (or press Enter to skip): ").lower()

        if (auto_task == 'true' and not config.auto_task) or (auto_task == 'false' and config.auto_task):
            cfg["auto_task"] = (auto_task == 'true')
            print(f"{green}Auto task config updated successfully!")
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(cfg, indent=4))
            print(f"\n{red}Auto task configuration has been reset based on your input.")
            input(f"\n{blue}Press Enter to continue...")
            return await main()

        # Auto game mode
        print(f"{ungu}{tebal}[{green}+{white}] Auto Play Game: {green}{config.auto_game}{white}")
        auto_game = input(f" {yellow} Enter True/False to change (or press Enter to skip): ").lower()

        if (auto_game == 'true' and not config.auto_game) or (auto_game == 'false' and config.auto_game):
            cfg["auto_game"] = (auto_game == 'true')
            print(f"{green}Auto game config updated successfully!")
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(cfg, indent=4))
            print(f"\n{red}Auto game configuration has been reset based on your input.")
            input(f"\n{blue}Press Enter to continue...")
            return await main()

        # Game point settings
        print(f"{ungu}{tebal}[{green}+{white}] Enter Game Point: {white}[{green}{config.low}{white}/{green}{config.high}{white}]")
        new_low = input(f"  {yellow} Enter new low point (or press Enter to skip): ")
        new_high = input(f" {yellow}  Enter new high point (or press Enter to skip): ")
        
        # If the user enters numbers for low and high, perform reset
        if new_low.isdigit() and new_high.isdigit():
            cfg["low"] = int(new_low)
            cfg["high"] = int(new_high)
            print(f"{green}Game point updated successfully!")
            
            async with aiofiles.open(config_file, "w") as w:
                await w.write(json.dumps(cfg, indent=4))
            print(f"\n{red}Game point configuration has been reset based on your input.")
            input(f"\n{blue}Press Enter to continue...")
            return await main()
        elif not new_low and not new_high:
            print(f"{blue}Skipped updating game point.")

        print(f"{ungu}{tebal}[{green}+{white}] Start bot mode: {green}Slowly {white}/ {green}Faster")
        mode = input(f"  {yellow} Choose mode (Slowly/Faster) or press Enter to skip: ").lower()

        # Save config changes
        async with aiofiles.open(config_file, "w") as w:
            await w.write(json.dumps(cfg, indent=4))

        if mode in ['slowly', 'faster']:
            if mode == "slowly":
                # Start bot in sync mode
                while True:
                    datas, proxies = await get_data(args.data, args.proxy)
                    result = []
                    for no, data in enumerate(datas):
                        res = await BlumAirdrop(
                            id=no, query=data, proxies=proxies, config=config
                        ).start()
                        result.append(res)
                    end = int(datetime.now().timestamp())
                    total = min(result) - end
                    await countdown(total)
            elif mode == "faster":
                # Start bot in multiprocessing mode
                if not args.worker:
                    worker = int(os.cpu_count() / 2)
                    if worker < 1:
                        worker = 1
                else:
                    worker = int(args.worker)
                sema = asyncio.Semaphore(worker)

                async def bound(sem, params):
                    async with sem:
                        return await BlumAirdrop(*params).start()

                while True:
                    datas, proxies = await get_data(args.data, args.proxy)
                    tasks = [
                        asyncio.create_task(bound(sema, (no, data, proxies, config)))
                        for no, data in enumerate(datas)
                    ]
                    result = await asyncio.gather(*tasks)
                    end = int(datetime.now().timestamp())
                    total = min(result) - end
                    await countdown(total)
        else:
            input(f"\n{blue}Press Enter to continue...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()