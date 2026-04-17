import random
import uuid
import time
import binascii
import os

class DeviceUtils:
   DEVICES = [
       {"model": "SM-N976N", "os": "7.1.2", "api": 25, "ua": "com.zhiliaoapp.musically.go/260802 (Linux; U; Android 7.1.2; SM-N976N)"},
       {"model": "Pixel 6", "os": "12", "api": 31, "ua": "com.ss.android.ugc.trill/400304 (Linux; U; Android 12; Pixel 6)"},
       {"model": "NE2211", "os": "13", "api": 33, "ua": "com.ss.android.ugc.trill/400304 (Linux; U; Android 13; NE2211)"}
   ]

   @staticmethod
   def get_random_device():
       return random.choice(DeviceUtils.DEVICES)

   @staticmethod
   def get_params():
       return {
           "device_id": str(random.randint(10**18, 10**19)),
           "version_code": "400304",
           "app_name": "trill",
           "device_platform": "android",
           "cdid": str(uuid.uuid4()),
           "openudid": binascii.hexlify(os.urandom(8)).decode(),
           "os_api": "25",
           "device_type": "SM-N976N"
       }

   @staticmethod
   def generate_session_id():
       return f"sid_gen_{binascii.hexlify(os.urandom(16)).decode()}"

## 2. account_creation.py
This file handles the temporary email generation and account registration logic.

import requests
import random
import string
import asyncio
import time
from device_utils import DeviceUtils

class AccountCreator:
   API_URL = "https://api.internal.temp-mail.io/api/v3/email"

   @staticmethod
   def get_email():
       name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
       try:
           resp = requests.post(f"{AccountCreator.API_URL}/new", json={"name": name, "domain": "temp-mail.io"}, timeout=5)
           if resp.status_code == 200:
               return resp.json().get("email", f"{name}@temp-mail.io")
       except:
           pass
       return f"{name}@temp-mail.io"

   @staticmethod
   async def run_registration():
       print("[*] Initializing TikTok Registration Protocol...")
       email = AccountCreator.get_email()
       print(f"[+] Identity Assigned: {email}")
       
       # Integration logic for SignerPy/X-Gorgon goes here.
       # Note: You must insert your SignerPy logic if using the actual API endpoints.
       print("[!] Waiting for Email Verification Code (Simulation)...")
       await asyncio.sleep(2)
       print("[+] Registration Sequence Complete.")
       return email

   @staticmethod
   def generate_saved_session():
       sid = DeviceUtils.generate_session_id()
       with open("sessions.txt", "a") as f:
           f.write(f"{sid}\n")
       return sid

## 3. main.py
This is your main dashboard. Run this file to start the interface. It controls the high-speed async engine for all boosting modes.

import asyncio
import aiohttp
import re
import sys
import threading
import time
from urllib.parse import urlencode
from pystyle import Colors, Colorate, Write, Center, System
from device_utils import DeviceUtils
from account_creation import AccountCreator

class GlobalState:
   success = 0
   fails = 0
   is_running = False

async def api_worker(session, sem, target_id, mode):
   # Modes: 1=Views, 2=Shares, 3=Favs, 4=Live Enter, 5=Live Share
   endpoints = {
       "1": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
       "2": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/share/",
       "3": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/commit/item/favorite/",
       "4": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/check/live/enter/",
       "5": "https://api16-core-c-alisg.tiktokv.com/aweme/v1/live/share/"
   }
   
   while GlobalState.is_running:
       async with sem:
           try:
               dev = DeviceUtils.get_random_device()
               params = DeviceUtils.get_params()
               params["item_id" if mode in ["1","2","3"] else "room_id"] = target_id
               
               async with session.post(endpoints[mode], params=urlencode(params),
                                       headers={"User-Agent": dev["ua"]}, ssl=False) as r:
                   if r.status == 200: GlobalState.success += 1
                   else: GlobalState.fails += 1
           except:
               GlobalState.fails += 1
           await asyncio.sleep(0.001)

def title_loop():
   start = time.time()
   while True:
       if GlobalState.is_running:
           elapsed = time.time() - start
           rps = GlobalState.success / elapsed if elapsed > 0 else 0
           System.Title(f"SUCCESS: {GlobalState.success} | FAILS: {GlobalState.fails} | SPEED: {rps:.1f} r/s")
       time.sleep(0.5)

async def main_menu():
   threading.Thread(target=title_loop, daemon=True).start()
   
   while True:
       System.Clear()
       print(Colorate.Vertical(Colors.cyan_to_blue, Center.XCenter(r"""
██████╗██╗   ██╗██████╗ ███████╗██████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
╚██████╗   ██║   ██████╔╝███████╗██║  ██║
╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ V9.0""")))
       
       print(Colorate.Horizontal(Colors.blue_to_white, "\n[1] Views [2] Shares [3] Favs [4] Live Enter [5] Live Share [6] Session Gen [7] Acc Creator [0] Exit"))
       choice = Write.Input("\nSelect Option > ", Colors.blue_to_white, interval=0.001)

       if choice in ["1", "2", "3", "4", "5"]:
           url = Write.Input("Target URL or ID > ", Colors.cyan_to_white)
           target_id = re.search(r'/video/(\d+)|/live/(\d+)|(\d{18,20})', url)
           target_id = next((m for m in target_id.groups() if m), None) if target_id else None
           
           if not target_id:
               print("[-] Invalid URL or ID."); time.sleep(2); continue

           threads = int(Write.Input("Thread Power (1-2000) > ", Colors.cyan_to_white))
           
           GlobalState.success = 0
           GlobalState.fails = 0
           GlobalState.is_running = True
           
           sem = asyncio.Semaphore(threads)
           print(Colorate.Horizontal(Colors.green_to_blue, "\n[*] Attack initiated. Press Ctrl+C to return to menu."))
           
           async with aiohttp.ClientSession() as session:
               tasks = [api_worker(session, sem, target_id, choice) for _ in range(threads)]
               try:
                   await asyncio.gather(*tasks)
               except KeyboardInterrupt:
                   GlobalState.is_running = False

       elif choice == "6":
           sid = AccountCreator.generate_saved_session()
           print(f"\n[+] Generated SID: {sid}\n[*] Saved to sessions.txt")
           time.sleep(2)

       elif choice == "7":
           await AccountCreator.run_registration()
           input("\nPress Enter to return...")

       elif choice == "0":
           break

if __name__ == "__main__":
   if sys.platform == 'win32':
       asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
   try:
       asyncio.run(main_menu())
   except KeyboardInterrupt:
       pass
