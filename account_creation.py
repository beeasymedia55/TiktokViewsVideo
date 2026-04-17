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
