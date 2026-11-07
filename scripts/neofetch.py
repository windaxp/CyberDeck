import subprocess
import os
import sys

# --- 📁 ПАПКИ В КОРНЕ (рядом со скриптом) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

def ensure_dirs():
    for d in [SCREENSHOTS_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

# --- ЦВЕТА ---
class C:
    CY = '\033[96m'
    G = '\033[92m'
    W = '\033[93m'
    F = '\033[91m'
    B = '\033[94m'
    E = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def adb(cmd):
    return subprocess.run(f"adb {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

def get_temperature():
    out = adb("shell dumpsys battery")
    for line in out.split('\n'):
        line = line.strip()
        if line.startswith("temperature:"):
            try: return int(line.split(":", 1)[1].strip()) / 10.0
            except ValueError: pass
    try:
        raw = adb("shell cat /sys/class/power_supply/battery/temp").strip()
        if raw.isdigit(): return int(raw) / 10.0
    except Exception: pass
    try:
        raw = adb("shell cat /sys/class/thermal/thermal_zone0/temp").strip()
        if raw.isdigit():
            v = int(raw)
            return v / 1000.0 if v > 1000 else v / 10.0
    except Exception: pass
    return None

def main():
    ensure_dirs()
    clear()

    if not any(line.strip().endswith("device") for line in adb("devices").split('\n')[1:] if line.strip()):
        print(f"{C.F}[!] Ошибка: Телефон не подключен по ADB!{C.E}")
        sys.exit()

    print(f"{C.CY}[*] Собираю системную информацию...{C.E}\n")

    brand = adb("shell getprop ro.product.brand").capitalize()
    model = adb("shell getprop ro.product.model").strip()
    android_ver = adb("shell getprop ro.build.version.release").strip()
    kernel = adb("shell uname -r").strip()
    uptime = adb("shell uptime").strip()
    res = adb("shell wm size").replace("Physical size: ", "").strip()

    battery = "?"
    for line in adb("shell dumpsys battery").split('\n'):
        line = line.strip()
        if line.startswith("level:"):
            battery = line.split(":", 1)[1].strip()
            break

    temp = get_temperature()
    temp_str = f"{temp:.1f}°C" if temp is not None else "N/A"

    cpu = adb("shell cat /proc/cpuinfo | grep Hardware").replace("Hardware", "").replace(":", "").strip()
    if not cpu: cpu = "ARM64 Processor"

    ram_total = adb("shell cat /proc/meminfo | grep MemTotal").split()
    if len(ram_total) > 1:
        ram_gb = int(ram_total[1]) / 1024 / 1024
        ram_str = f"{ram_gb:.1f} GB"
    else:
        ram_str = "Unknown"

    logo = f"""{C.F}        ┌─────────────────────┐{C.E}
{C.F}        │  {C.B}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄{C.F}  │{C.E}
{C.F}        │  {C.B}█               █{C.F}  │{C.E}
{C.F}        │  {C.B}█   {C.F}◉       ◉{C.B}   █{C.F}  │{C.E}
{C.F}        │  {C.B}█               █{C.F}  │{C.E}
{C.F}        │  {C.B}█    {C.F}▄▄▄▄▄▄▄{C.B}    █{C.F}  │{C.E}
{C.F}        │  {C.B}█    {C.F}█ █ █ █{C.B}    █{C.F}  │{C.E}
{C.F}        │  {C.B}█    {C.F}▀▀▀▀▀▀▀{C.B}    █{C.F}  │{C.E}
{C.F}        │  {C.B}█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█{C.F}  │{C.E}
{C.F}        └──────────{C.B}┬{C.F}──────────┘{C.E}
{C.F}                   {C.B}│{C.E}
{C.F}                 {C.B}═══╧═══{C.E}"""

    info = f"""{C.CY}{C.BOLD}user{C.E}@{C.CY}{C.BOLD}cyberdeck{C.E}
{C.CY}───────────────────────{C.E}
{C.G}OS{C.E}:       Android {android_ver}
{C.G}Device{C.E}:   {brand} {model}
{C.G}Kernel{C.E}:   {kernel}
{C.G}Uptime{C.E}:   {uptime}
{C.G}Battery{C.E}:  {battery}%
{C.G}Temp{C.E}:     {temp_str}
{C.G}Screen{C.E}:   {res}
{C.G}CPU{C.E}:      {cpu}
{C.G}RAM{C.E}:      {ram_str}"""

    logo_lines = logo.split('\n')
    info_lines = info.split('\n')
    max_lines = max(len(logo_lines), len(info_lines))

    for i in range(max_lines):
        l_line = logo_lines[i] if i < len(logo_lines) else " " * 30
        i_line = info_lines[i] if i < len(info_lines) else ""
        print(f"  {l_line}   {i_line}")

    print("\n")
    input(f"{C.W}Нажми Enter, чтобы выйти...{C.E}")

if __name__ == "__main__":
    main()
