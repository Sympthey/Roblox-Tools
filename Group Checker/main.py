"""
Attempt to import our packages, if failed it means the user did not install them so tell them how to.
"""
import os, json, ctypes
try:
    import aiohttp, asyncio
    from colorama import *
except:
    os.system("pip install requirements.txt")
    print("[X] Packages Missing! Please rerun the program now they are installed.")
init()

"""
Some variables for our async start.
"""
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)


class GroupChecker:
    def __init__(self):
        """
        Going to define some colors from colorama so I dont need to retype them all the dam time :)
        """
        self.green = Fore.GREEN
        self.red = Fore.RED
        self.reset = Fore.RESET
        """
        Define some vars for out title updater later on
        """
        self.checked = 0
        self.taken = 0
        self.available = 0

    def read_file(self, path):
        names = []
        groupsToCheck = open(path, "r")
        groupsToCheck = groupsToCheck.readlines()
        for name in groupsToCheck:
            names.append(name.strip())
        return names

    async def check_taken(self, name):
        """
        This is the actualy function which hits the roblox lookup API and checks if there is a valid group with the name.
        """
        headers = {
            # We will be nice and pass some headers to the api endpoint.
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 OPR/72.0.3815.320",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
        }
        async with aiohttp.ClientSession() as hit_endpoint:
            send_req = await hit_endpoint.get(f"https://groups.roblox.com/v1/groups/search/lookup?groupName={name}", headers=headers)
            get_json = await send_req.text()
            parse_json = json.loads(get_json)
            await asyncio.sleep(0.0025)
            try:
                if parse_json['data'][0]['name'].lower() == name.lower():
                    print(self.red+f"[{name}] --> Taken")
                    self.taken += 1
                else:
                    print(self.green+f"[{name}] --> Available")
                    self.available += 1
            except:
                print(self.green+f"[{name}] --> Available")
                self.available += 1
            self.checked += 1
            self.title()

    def title(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"[Roblox Group Checker] Developer Sympthey#9308 | Checked {self.checked} | Taken {self.taken} | Available {self.available}")

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    path = os.getcwd()
    _instance = GroupChecker()
    account = _instance.read_file(f"{path}/names.txt")
    for chunk in chunks(account, 550):
        tries = asyncio.gather(*[_instance.check_taken(account) for account in chunk])
        loop.run_until_complete(tries)
        asyncio.sleep(0.25)
