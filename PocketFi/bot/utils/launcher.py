import os
import glob
import asyncio
import argparse
from itertools import cycle

from pyrogram import Client
from better_proxy import Proxy
from colorama import Fore, Style, init
from bot.config import settings
from bot.utils import logger
from bot.core.claimer import run_claimer
from bot.core.registrator import register_sessions

# Initialize colorama
init(autoreset=False)

# Define start text with color formatting
start_text = f"""
{Fore.GREEN}{Style.BRIGHT} ███{Fore.MAGENTA}╗{Fore.GREEN}   ██{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN}███████{Fore.MAGENTA}╗{Fore.GREEN} ██████{Fore.MAGENTA}╗
{Fore.CYAN} ████{Fore.MAGENTA}╗{Fore.CYAN}  ██{Fore.MAGENTA}║{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝{Fore.CYAN}██{Fore.MAGENTA}╔════╝
{Fore.CYAN} ██{Fore.MAGENTA}╔{Fore.CYAN}██{Fore.MAGENTA}╗{Fore.CYAN} ██{Fore.MAGENTA}║{Fore.CYAN}█████{Fore.MAGENTA}╗{Fore.CYAN}  █████{Fore.MAGENTA}╗{Fore.CYAN}  ███████{Fore.MAGENTA}╗{Fore.CYAN}██{Fore.MAGENTA}║{Fore.CYAN}     
{Fore.BLUE} ██{Fore.MAGENTA}║╚{Fore.BLUE}██{Fore.MAGENTA}╗{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}╔══╝{Fore.BLUE}  ██{Fore.MAGENTA}╔══╝{Fore.BLUE}  {Fore.MAGENTA}╚════{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}██{Fore.MAGENTA}║{Fore.BLUE}     
{Fore.BLUE} ██{Fore.MAGENTA}║ ╚{Fore.BLUE}████{Fore.MAGENTA}║{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}╗{Fore.BLUE}███████{Fore.MAGENTA}║╚{Fore.BLUE}██████{Fore.MAGENTA}╗
{Fore.MAGENTA} ╚═╝  ╚═══╝╚══════╝╚══════╝╚══════╝ ╚═════╝{Fore.RED} For Free 🔥 
{Fore.YELLOW}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[⭐] {Fore.GREEN}[Dev. By @nee.z.c]        {Fore.YELLOW}                       ┃
{Fore.YELLOW}{Style.BRIGHT}┃{Fore.MAGENTA}[❄️] {Fore.CYAN}[Airdrop PocketFi]          {Fore.YELLOW}                     ┃
{Fore.YELLOW}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

"""

def get_session_names() -> list[str]:
    """Retrieve session names from session files."""
    session_names = glob.glob('sessions/*.session')
    session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]
    return session_names

def get_proxies() -> list[str]:
    """Retrieve proxies from file if specified in settings."""
    proxies = []
    if settings.USE_PROXY_FROM_FILE:
        try:
            with open('bot/config/proxies.txt', encoding='utf-8-sig') as file:
                proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file if row.strip()]
        except FileNotFoundError:
            logger.warning("Proxies file not found.")
        except Exception as e:
            logger.error(f"An error occurred while reading proxies file: {e}")
    return proxies

async def get_tg_clients() -> list[Client]:
    """Initialize and return a list of Pyrogram Client instances."""
    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Session files not found.")

    if not settings.API_ID or not settings.API_HASH:
        raise ValueError("API_ID and API_HASH not found in the .env file.")

    tg_clients = [Client(
        name=session_name,
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        workdir='sessions/',
        plugins=dict(root='bot/plugins')
    ) for session_name in session_names]

    return tg_clients

async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")

    logger.info(f"Detected {len(get_session_names())} sessions | {len(get_proxies())} proxies")

    action = parser.parse_args().action

    if not action:
        print(start_text)

        while True:
            action = input("Are you ready to start? (y/n): ").lower()

            if action not in ["y", "n"]:
                logger.warning("Please choose 'y' for Yes or 'n' for No")
            else:
                break

    if action == "n":
        await register_sessions()  # This will act as "login" in your context
    elif action == "y":
        tg_clients = await get_tg_clients()
        await run_tasks(tg_clients=tg_clients)

async def run_tasks(tg_clients: list[Client]) -> None:
    """Run tasks for each client with optional proxy rotation."""
    proxies = get_proxies()
    proxies_cycle = cycle(proxies) if proxies else None
    tasks = [asyncio.create_task(run_claimer(tg_client=tg_client, proxy=next(proxies_cycle) if proxies_cycle else None))
             for tg_client in tg_clients]

    await asyncio.gather(*tasks)

