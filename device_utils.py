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
