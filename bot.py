#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Viewer V2 - Versi Premium
===================================
- Auto install library
- Dioptimalkan untuk kecepatan maksimal
"""
import subprocess
import sys

REQUIRED_PACKAGES = {
    "aiohttp": "aiohttp>=3.9.0",
    "requests": "requests>=2.31.0"
}

def install(pkg):
    try:
        print(f"📦 Sedang install {pkg} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])
    except Exception as e:
        print(f"❌ Error install {pkg}: {e}")

# Auto install library jika kurang
for module, pkg in REQUIRED_PACKAGES.items():
    try:
        __import__(module)
        print(f"✔ {pkg} sudah ada!")
    except ImportError:
        print(f"⚠ Kurang {pkg} → Install sekarang...")
        install(pkg)

# ===============================================
# KODE UTAMA - VERSI INDONESIA + OPTIMASI
# ===============================================
import os
os.environ['AIOHTTP_NO_EXTENSIONS'] = '1'

import sys
if sys.version_info < (3, 8):
    print("❌ Python 3.8+ diperlukan!")
    sys.exit(1)

import aiohttp
import asyncio
import random
import requests
import re
import time
import secrets
import signal
from hashlib import md5
from time import time as T
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass, field
from collections import deque
from urllib.parse import urlencode
import logging
import socket
import json
import threading

PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

# Non-aktifkan logging untuk kecepatan
logging.basicConfig(level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# OPTIMASI: Cache endpoint yang sering dipakai
VIEW_ENDPOINTS = [
    "https://api16-core-c-alisg.tiktokv.com/aweme/v1/aweme/stats/",
    "https://api16-core-c-useast1a.tiktokv.com/aweme/v1/aweme/stats/",
    "https://api16-core-c.tiktokv.com/aweme/v1/aweme/stats/",
    "https://api16-va.tiktokv.com/aweme/v1/aweme/stats/",
    "https://api16-va-alisg.tiktokv.com/aweme/v1/aweme/stats/",
    "https://api16-core.tiktokv.com/aweme/v1/aweme/stats/",
]

VERSION_CODES = ["400304", "400305", "400306", "400307"]
AIDS = ["1233", "1234", "1235", "1180"]
CHANNELS = ["googleplay", "appstore", "tiktok_ads"]
DEVICE_BRANDS = ['Google', 'Samsung', 'Xiaomi', 'Oppo', 'OnePlus', 'Realme', 'Vivo',
                 'Huawei', 'Honor', 'Motorola', 'Nokia', 'Sony', 'Asus', 'Tecno',
                 'Infinix', 'TCL', 'Nothing', 'Redmi', 'Poco', 'Meizu', 'Lenovo']
APP_LANGUAGES = ['vi', 'en', 'zh', 'th', 'id', 'ms', 'ja', 'ko', 'es', 'fr', 'de', 'pt']
REGIONS = ['VN', 'US', 'SG', 'MY', 'TH', 'ID', 'PH', 'TW', 'JP', 'KR', 'GB', 'DE', 'FR', 'ES', 'BR']
TIMEZONES = [
    'Asia%2FHo_Chi_Minh', 'America%2FNew_York', 'Asia%2FSingapore',
    'Asia%2FBangkok', 'Asia%2FKuala_Lumpur', 'Asia%2FJakarta', 'Asia%2FManila',
    'Asia%2FTokyo', 'Asia%2FSeoul', 'Europe%2FLondon', 'Europe%2FBerlin',
    'Europe%2FParis', 'Europe%2FMadrid', 'America%2FSao_Paulo'
]

# OPTIMASI: Pre-defined combinations untuk akses cepat
SCREEN_PRESETS = [
    (720, 1600, 320),
    (1080, 1920, 420),
    (1080, 2340, 400),
]
RAM_SIZES = [4, 6, 8]

@dataclass
class DeviceInfo:
    """Info device sederhana & cepat"""
    device_id: int
    iid: int
    brand: str
    model: str
    version: str
    api_level: int

class DeviceGenerator:
    """Generator device yang dioptimalkan untuk kecepatan"""
    
    BRANDS = DEVICE_BRANDS
    ANDROID_VERSIONS = {"11": 30, "12": 31, "13": 33}
    
    # Pre-generate device pool
    _device_pool = deque(maxlen=1000000)
    _lock = threading.Lock()
    _session_id = int(time.time() * 1000)
    
    @classmethod
    def generate_device(cls) -> DeviceInfo:
        """Generate 1 device - super cepat"""
        brand = random.choice(cls.BRANDS)
        version = random.choice(list(cls.ANDROID_VERSIONS.keys()))
        api_level = cls.ANDROID_VERSIONS[version]
        
        # Device ID unik
        device_id = (random.randint(600000000000000, 999999999999999) + cls._session_id) % 999999999999999
        iid = (random.randint(7000000000000000000, 7999999999999999999) + cls._session_id) % 7999999999999999999
        
        return DeviceInfo(
            device_id=device_id,
            iid=iid,
            brand=brand,
            model=f"{brand} Phone",
            version=version,
            api_level=api_level
        )
    
    @classmethod
    def pre_generate(cls, count: int = 100000):
        """Pre-generate devices di background"""
        print(f"🔄 Pre-generate {count:,} devices...")
        for i in range(count):
            with cls._lock:
                cls._device_pool.append(cls.generate_device())
        print(f"✅ Siap: {len(cls._device_pool):,} devices")
    
    @classmethod
    def get_device(cls) -> DeviceInfo:
        """Ambil device dari pool (cepat)"""
        with cls._lock:
            if cls._device_pool:
                return cls._device_pool.popleft()
            return cls.generate_device()

class Signature:
    """Generate signature super cepat"""
    
    def __init__(self, params: str):
        self.params = params
    
    def generate(self) -> Dict[str, str]:
        """Generate X-Gorgon cepat"""
        timestamp = int(T())
        # Signature sederhana untuk kecepatan
        signature = md5(f"{self.params}{timestamp}".encode()).hexdigest()[:16]
        
        return {
            "X-Gorgon": "840280416000" + signature,
            "X-Khronos": str(timestamp)
        }

class TikTokViewerV2:
    """TikTok Viewer - Versi Indonesia + Optimasi Kecepatan"""
    
    def __init__(self, views_per_minute: int = 100):
        self.views_per_minute = views_per_minute
        self.delay = 60.0 / views_per_minute
        
        # Counter
        self.count = 0
        self.success = 0
        self.failed = 0
        self.start_time = 0
        self.is_running = False
        self.session = None
        
        # OPTIMASI: Cache untuk video yang sudah diproses
        self.video_cache = {}
        
        # OPTIMASI: Pre-generate devices
        DeviceGenerator.pre_generate(50000)
    
    async def init_session(self):
        """Init session dengan optimasi maksimal"""
        timeout = aiohttp.ClientTimeout(total=8, connect=2)
        connector = aiohttp.TCPConnector(
            limit=1000,
            ttl_dns_cache=300,
            use_dns_cache=True,
            force_close=False
        )
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'User-Agent': 'com.ss.android.ugc.trill/400304'},
            skip_auto_headers={'User-Agent'}
        )
    
    async def close_session(self):
        """Tutup session"""
        if self.session:
            await self.session.close()
    
    def get_video_id(self, url: str) -> Optional[str]:
        """Ekstrak video ID - super cepat dengan cache"""
        # Cek cache dulu
        if url in self.video_cache:
            return self.video_cache[url]
        
        try:
            # Pattern cepat
            match = re.search(r'/video/(\d+)', url)
            if match:
                video_id = match.group(1)
                self.video_cache[url] = video_id
                return video_id
            
            # Pattern alternatif
            match = re.search(r'(\d{19})', url)
            if match:
                video_id = match.group(1)
                self.video_cache[url] = video_id
                return video_id
            
            # Fallback ke requests (jarang)
            r = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            match = re.search(r'"id":"(\d{19})"', r.text)
            if match:
                video_id = match.group(1)
                self.video_cache[url] = video_id
                return video_id
            
            return None
        except:
            return None
    
    def generate_view_data(self, video_id: str, device: DeviceInfo) -> Tuple[str, Dict, Dict]:
        """Generate data view - minimalis untuk kecepatan"""
        
        # Parameter sederhana
        params = (
            f"channel=googleplay&aid=1233&version_code=400304"
            f"&device_id={device.device_id}&iid={device.iid}"
            f"&os_api={device.api_level}&os_version={device.version}"
            f"&device_brand={device.brand}&device_type=Phone"
            f"&app_language=id&region=ID&tz_name=Asia%2FJakarta"
        )
        
        url = f"{random.choice(VIEW_ENDPOINTS)}?{params}"
        
        # Data minimal
        data = {
            "item_id": video_id,
            "play_delta": 1,
            "play_time": random.randint(15, 45)
        }
        
        return url, data, {}
    
    async def send_view(self, video_id: str) -> bool:
        """Kirim 1 view - secepat mungkin"""
        try:
            device = DeviceGenerator.get_device()
            url, data, cookies = self.generate_view_data(video_id, device)
            
            # Generate signature
            sig = Signature(url.split('?')[1] if '?' in url else '').generate()
            
            # Kirim request
            async with self.session.post(
                url,
                data=urlencode(data),
                headers={**sig, 'Content-Type': 'application/x-www-form-urlencoded'},
                ssl=False,
                timeout=5
            ) as resp:
                if resp.status == 200:
                    self.count += 1
                    self.success += 1
                    return True
                else:
                    self.failed += 1
                    return False
                
        except Exception:
            self.failed += 1
            return False
    
    async def worker(self, video_id: str):
        """Worker untuk kirim view terus menerus"""
        while self.is_running:
            await self.send_view(video_id)
            # Delay dinamis berdasarkan kecepatan yang diinginkan
            await asyncio.sleep(self.delay / 100)  # 100 concurrent workers
    
    async def run(self, video_url: str):
        """Jalankan viewer"""
        print("\n" + "="*60)
        print("🚀 TIKTOK VIEWER V2 - INDONESIA")
        print("="*60)
        print(f"🎯 Target: {self.views_per_minute} view/menit")
        print(f"⚡ Mode: Super Cepat (Optimasi)")
        print("="*60)
        
        # Ambil video ID
        print("\n🔍 Mendapatkan Video ID...", end="", flush=True)
        video_id = self.get_video_id(video_url)
        
        if not video_id:
            print(" ❌ GAGAL")
            print("URL tidak valid!")
            return
        
        print(f" ✅ {video_id}")
        
        # Inisialisasi
        print("⚙️  Inisialisasi sistem...", end="", flush=True)
        await self.init_session()
        self.is_running = True
        self.start_time = time.time()
        print(" ✅")
        
        # Jalankan workers (100 concurrent)
        workers = 100
        print(f"👥 Menjalankan {workers} workers...")
        
        tasks = [asyncio.create_task(self.worker(video_id)) for _ in range(workers)]
        
        # Monitor progress
        try:
            last_count = 0
            while self.is_running:
                await asyncio.sleep(2)
                
                # Hitung kecepatan
                now = time.time()
                elapsed = now - self.start_time
                current_speed = (self.count - last_count) / 2 * 60  # views per menit
                last_count = self.count
                
                # Tampilkan stats
                total = self.success + self.failed
                success_rate = (self.success / total * 100) if total > 0 else 0
                
                print(
                    f"\r📊 Views: {self.count:,} | "
                    f"⚡ {current_speed:.0f}/menit | "
                    f"✅ {success_rate:.1f}% | "
                    f"⌛ {elapsed:.0f}s",
                    end="", flush=True
                )
                
        except KeyboardInterrupt:
            print("\n\n🛑 Memberhentikan...")
        finally:
            self.is_running = False
            
            # Cancel tasks
            for task in tasks:
                task.cancel()
            
            await asyncio.gather(*tasks, return_exceptions=True)
            await self.close_session()
            
            # Tampilkan hasil akhir
            elapsed = time.time() - self.start_time
            avg_speed = (self.count / elapsed) * 60 if elapsed > 0 else 0
            
            print("\n" + "="*60)
            print("📊 HASIL AKHIR")
            print("="*60)
            print(f"👀 Total view: {self.count:,}")
            print(f"⏰ Waktu: {elapsed:.1f} detik ({elapsed/60:.1f} menit)")
            print(f"📈 Rata-rata: {avg_speed:.0f} view/menit")
            print(f"✅ Sukses: {self.success:,}")
            print(f"❌ Gagal: {self.failed:,}")
            print("="*60)

def main():
    """Main program - Sederhana & Cepat"""
    
    print("\n" + "="*60)
    print("🎥 TIKTOK VIEWER - INDONESIA")
    print("="*60)
    print("Cara pakai: Masukkan URL video")
    print("Contoh: https://www.tiktok.com/@user/video/123456789")
    print("="*60)
    
    # Input URL
    url = input("\n📌 URL TikTok: ").strip()
    
    if not url:
        print("❌ URL tidak boleh kosong!")
        return
    
    # Pilih kecepatan
    print("\n⚡ Pilih kecepatan:")
    print("1. Lambat (50 view/menit) - Aman")
    print("2. Sedang (200 view/menit) - Normal")
    print("3. Cepat (500 view/menit) - Cepat")
    print("4. Turbo (1000 view/menit) - Resiko tinggi")
    
    choice = input("Pilih (1-4) [2]: ").strip() or "2"
    
    speed_map = {
        "1": 50,
        "2": 200,
        "3": 500,
        "4": 1000
    }
    
    views_per_minute = speed_map.get(choice, 200)
    
    # Konfirmasi
    print(f"\n✅ URL: {url[:60]}..." if len(url) > 60 else f"\n✅ URL: {url}")
    print(f"⚡ Kecepatan: {views_per_minute} view/menit")
    
    input("\n⏎ Tekan Enter untuk mulai (Ctrl+C untuk stop)...")
    
    # Jalankan
    viewer = TikTokViewerV2(views_per_minute=views_per_minute)
    
    try:
        asyncio.run(viewer.run(url))
    except KeyboardInterrupt:
        print("\n\n👋 Selesai!")
    except Exception as e:
        print(f"\n💥 Error: {e}")

if __name__ == "__main__":
    main()
