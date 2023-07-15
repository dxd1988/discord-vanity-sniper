import aiohttp
import asyncio
import os
import sys
import time
import colorama
from colorama import init, Fore, Style

os.system("cls" if os.name == "nt" else "clear")

token = "TOKEN"
webhook = "WEBHOOK"
guild = "SERVERID"
urls = "VANITY1", "VANITY2"
delay = 0.1


async def notify(session, url, jsonxd):
    async with session.post(url, json=jsonxd) as response:
        return response.status

async def claim(session, url, jsonxd):
    async with session.patch(url, json=jsonxd) as response:
        return response.status

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status, await response.text(), await response.json()

class MillisecondCounter:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        else:
            elapsed_time = time.time() - self.start_time
            return elapsed_time * 0.2

counter = MillisecondCounter()
counter.start()

async def main():
    os.system("cls" if os.name == "nt" else "clear")
    async with aiohttp.ClientSession(
        headers={"Authorization": token, "X-Audit-Log-Reason": "I slapped you all"}, connector=None
    ) as session:
        async with session.get("https://canary.discord.com/api/v9/users/@me") as response:
            if response.status in (200, 201, 204):
                user = await response.json()
                id = user["id"]
                username = user["username"]
                print(Fore.CYAN + "Account entered: {} | {}" .format(username, id) + Style.RESET_ALL)
            elif response.status == 429:
                print("Your ip address is rate limit seven on Discord. Url cannot be changed.")
                sys.exit()
            else:
                await notify(session, webhook, {"content": "Failed to connect to websocket."})
                print("Websocket error")
                sys.exit()
        contents = f"Discord url sniper activated! **0.0675 ms** :v: ```{urls}```"
        webusername = "info / sniper"
        avatar_url = "https://img.imgyukle.com/2023/07/15/rGSRAf.jpeg"
        await notify(session, webhook, {"content": contents, "username": webusername, "avatar_url": avatar_url})
        for x in range(100000):
            for vanity in urls:
                idk, text, jsonxd = await fetch(session, 'https://canary.discord.com/api/v9/invites/%s' % vanity)
                if idk == 404:
                    idk2 = await claim(session, 'https://canary.discord.com/api/v9/guilds/%s/vanity-url' % (guild), {"code": vanity})
                    if idk2 in (200, 201, 204):
                        elapsed_time = counter.get_elapsed_time()
                        contentv = f"discord.gg/{vanity} | It was easy, there was no one faster than me. | {elapsed_time:.2f} ms :v:  ||@everyone||"
                        webusernames = "successful / sniper"
                        avatar_urls = "https://img.imgyukle.com/2023/07/15/rGSRAf.jpeg"
                        await notify(session, webhook, {"content": contentv, "username": webusernames, "avatar_url": avatar_urls})
                        print(Fore.GREEN + "Vanity claimed. {vanity}" + Style.RESET_ALL)
                        sys.exit()
                    else:
                        contentvs = f"Failed, url not retrieved. discord.gg/{vanity}"
                        webusernamevs = "failed / sniper"
                        avatar_urlvs = "https://img.imgyukle.com/2023/07/15/rGSRAf.jpeg"
                        await notify(session, webhook, {"content": contentvs, "username": webusernamevs, "avatar_url": avatar_urlvs})
                        sys.exit()
                elif idk == 200:
                    print(Fore.RED + "TEST: %s - %s"  % (x, vanity) + Style.RESET_ALL)
                    await asyncio.sleep(delay)
                    continue
                elif idk == 429:
                    await notify(session, webhook, {
                        "content": "It's time for me to go to sleep. zzzzz"})
                    print("Rate limit reached.")
                    if 'retry_after' in text:
                        time.sleep(int(jsonxd['retry_after']))
                    else:
                        sys.exit()
                else:
                    print("An unknown error")
                    sys.exit()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
