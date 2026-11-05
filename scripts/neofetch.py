import subprocess
import os
import sys

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

def main():
    clear()
    
    # Проверка подключения
    if not any(line.strip().endswith("device") for line in adb("devices").split('\n')[1:] if line.strip()):
        print(f"{C.F}[!] Ошибка: Телефон не подключен по ADB!{C.E}")
        sys.exit()

    print(f"{C.CY}[*] Собираю системную информацию...{C.E}\n")
    
    # Получаем данные
    brand = adb("shell getprop ro.product.brand").capitalize()
    model = adb("shell getprop ro.product.model").strip()
    android_ver = adb("shell getprop ro.build.version.release").strip()
    kernel = adb("shell uname -r").strip()
    uptime = adb("shell uptime").strip()
    battery = adb("shell dumpsys battery | grep level").replace("level:", "").strip()
    res = adb("shell wm size").replace("Physical size: ", "").strip()
    
    cpu = adb("shell cat /proc/cpuinfo | grep Hardware").replace("Hardware", "").replace(":", "").strip()
    if not cpu:
        cpu = "ARM64 Processor"
        
    ram_total = adb("shell cat /proc/meminfo | grep MemTotal").split()
    if len(ram_total) > 1:
        ram_gb = int(ram_total[1]) / 1024 / 1024
        ram_str = f"{ram_gb:.1f} GB"
    else:
        ram_str = "Unknown"

    # Твой фирменный логотип (Красный и Белый)
    logo = f"""{C.F}         .─────────────────.{C.E}
{C.F}       .'   {C.B}▄▄▄▄▄▄▄▄▄▄▄▄▄{C.F}   '.{C.E}
{C.F}      /    {C.B}█▀▀▀▀▀▀▀▀▀▀▀▀▀█{C.F}    \\{C.E}
{C.F}     |     {C.B}█             █{C.F}     |{C.E}
{C.F}     |     {C.B}█      {C.F}✦      {C.B}█{C.F}     |{C.E}
{C.F}     |     {C.B}█             █{C.F}     |{C.E}
{C.F}      \\    {C.B}█▄▄▄▄▄▄▄▄▄▄▄▄▄█{C.F}    /{C.E}
{C.F}       '.   {C.B}▀▀▀▀▀▀▀▀▀▀▀▀▀{C.F}   .'{C.E}
{C.F}         '─────────────────'{C.E}"""

    # Информация (справа)
    info = f"""{C.CY}{C.BOLD}user{C.E}@{C.CY}{C.BOLD}cyberdeck{C.E}
{C.CY}-----------------------{C.E}
{C.G}OS{C.E}: Android {android_ver}
{C.G}Device{C.E}: {brand} {model}
{C.G}Kernel{C.E}: {kernel}
{C.G}Uptime{C.E}: {uptime}
{C.G}Battery{C.E}: {battery}%
{C.G}Screen{C.E}: {res}
{C.G}CPU{C.E}: {cpu}
{C.G}RAM{C.E}: {ram_str}"""

    # Склеиваем построчно, чтобы логотип был слева, а текст справа
    logo_lines = logo.split('\n')
    info_lines = info.split('\n')
    max_lines = max(len(logo_lines), len(info_lines))
    
    for i in range(max_lines):
        l_line = logo_lines[i] if i < len(logo_lines) else " " * 28
        i_line = info_lines[i] if i < len(info_lines) else ""
        print(f"  {l_line}   {i_line}")
        
    print("\n")
    input(f"{C.W}Нажми Enter, чтобы выйти...{C.E}")

if __name__ == "__main__":
    main()
