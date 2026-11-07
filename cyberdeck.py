import os
import subprocess
import sys
import time
import random
import shutil
import glob

# --- 📁 ПАПКИ ПРЯМО В КОРНЕ СО СКРИПТОМ ---
def get_base_dir():
    # Папка, где физически лежит cyberdeck.py (корень)
    return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
SCREAMS_DIR = os.path.join(BASE_DIR, "screams")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

# 🔧 Создаём ВСЕ папки в корне, если их нет
def setup_folders():
    for folder in [SCREAMS_DIR, LOGS_DIR, SCREENSHOTS_DIR, SCRIPTS_DIR, BACKUP_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[+] Создана папка: {os.path.basename(folder)}/")

# --- ЦВЕТА ---
class C:
    H = '\033[95m'
    B = '\033[94m'
    CY = '\033[96m'
    G = '\033[92m'
    W = '\033[93m'
    F = '\033[91m'
    E = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def adb(cmd):
    result = subprocess.run(f"adb {cmd}", shell=True, capture_output=True, text=True)
    return result.stdout.strip() + result.stderr.strip()

def check_connection():
    out = adb("devices")
    for line in out.split('\n'):
        if line.strip().endswith("device"):
            return True
    return False

# --- УНИВЕРСАЛЬНЫЙ ДЕБЛОАТ ---
def debloat():
    print(f"\n{C.CY}[*] Определяю бренд устройства...{C.E}")
    brand_raw = adb("shell getprop ro.product.brand").strip().lower()
    model = adb("shell getprop ro.product.model").strip()

    DEBLOAT_DB = {
        "xiaomi": ["com.miui.msa.global", "com.miui.analytics", "com.xiaomi.mipicks", "com.miui.systemAdSolution", "com.xiaomi.discover", "com.xiaomi.joyose"],
        "samsung": ["com.samsung.android.app.spage", "com.samsung.android.bixby.agent", "com.samsung.android.game.gamehome", "com.samsung.android.app.tips", "com.samsung.android.mateagent"],
        "tecno": ["com.transsion.buzz", "com.transsion.phoenix", "com.transsion.faceid", "com.transsion.phonemaster", "com.transsion.carlcare"],
        "infinix": ["com.transsion.buzz", "com.transsion.phoenix", "com.transsion.faceid", "com.transsion.phonemaster", "com.transsion.carlcare"],
        "generic": ["com.google.android.apps.wellbeing", "com.google.android.feedback"]
    }

    brand_key = "generic"
    if any(x in brand_raw for x in ["redmi", "poco", "xiaomi"]): brand_key = "xiaomi"
    elif "samsung" in brand_raw: brand_key = "samsung"
    elif "tecno" in brand_raw: brand_key = "tecno"
    elif "infinix" in brand_raw: brand_key = "infinix"

    pkgs = DEBLOAT_DB[brand_key]

    print(f"{C.G}[+] Устройство: {brand_raw.capitalize()} {model}{C.E}")
    print(f"{C.W}[*] Найдено пакетов: {len(pkgs)}{C.E}")

    if input(f"{C.F}Удаляем? (y/n): {C.E}").lower() != 'y':
        print(f"{C.W}[i] Отменено.{C.E}"); input(); return

    success_count = 0
    for p in pkgs:
        print(f"  Удаляю: {p}...", end="", flush=True)
        res = adb(f"shell pm uninstall --user 0 {p}")
        if "Success" in res:
            print(f" {C.G}[OK]{C.E}"); success_count += 1
        else:
            print(f" {C.W}[НЕТ]{C.E}")

    print(f"\n{C.G}[+] Удалено: {success_count}/{len(pkgs)}{C.E}")
    input("Нажми Enter...")

# --- ЗАПУСК СКРИПТОВ ТОЛЬКО ИЗ scripts/ ---
def launch_script(script_name):
    path = os.path.join(SCRIPTS_DIR, script_name)
    if os.path.exists(path):
        subprocess.run([sys.executable, path])
    else:
        print(f"\n{C.F}[!] Скрипт scripts/{script_name} не найден!{C.E}")
        input()

def file_explorer():
    current_dir = BASE_DIR
    while True:
        clear()
        print(f"{C.CY}{C.BOLD}=== 📁 ПРОВОДНИК ==={C.E}")
        print(f"{C.W}Папка: {current_dir}{C.E}\n")
        try:
            items = os.listdir(current_dir)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x.lower()))
        except PermissionError:
            print(f"{C.F}[!] Нет доступа.{C.E}"); input(); current_dir = BASE_DIR; continue

        if not items: print(f"{C.W}Пусто.{C.E}")
        for i, item in enumerate(items, 1):
            path = os.path.join(current_dir, item)
            if os.path.isdir(path): print(f"  {C.B}[{i}] 📁 {item}/{C.E}")
            else:
                try: print(f"  {C.G}[{i}] 📄 {item} ({os.path.getsize(path)/1024:.1f} KB){C.E}")
                except OSError: print(f"  {C.G}[{i}] 📄 {item}{C.E}")

        print(f"\n{C.W}[номер] - зайти, del [номер] - удалить, cd [путь] - перейти, 0 - выход{C.E}")
        cmd = input(f"\n{C.BOLD}Проводник > {C.E}").strip().split()

        if not cmd: continue
        if cmd[0] == '0': break
        elif cmd[0].lower() == 'cd' and len(cmd) > 1:
            new_dir = " ".join(cmd[1:])
            if os.path.exists(new_dir) and os.path.isdir(new_dir): current_dir = new_dir
            else: print(f"{C.F}[!] Не найдено.{C.E}"); time.sleep(1)
        elif cmd[0].lower() == 'del' and len(cmd) > 1:
            try:
                idx = int(cmd[1]) - 1
                if 0 <= idx < len(items):
                    target = os.path.join(current_dir, items[idx])
                    if os.path.isdir(target): print(f"{C.F}[!] Это папка.{C.E}")
                    else: os.remove(target); print(f"{C.G}[+] Удален: {items[idx]}{C.E}")
            except: print(f"{C.F}[!] Ошибка.{C.E}")
            time.sleep(1)
        elif cmd[0].isdigit():
            idx = int(cmd[0]) - 1
            if 0 <= idx < len(items):
                target = os.path.join(current_dir, items[idx])
                if os.path.isdir(target): current_dir = target

def cleaner():
    clear(); print(f"{C.F}{C.BOLD}=== 🧹 ОЧИСТКА ==={C.E}\n")
    screens = glob.glob(os.path.join(SCREENSHOTS_DIR, "*"))
    if screens:
        for f in screens: os.remove(f)
        print(f"{C.G}[+] Удалено скриншотов: {len(screens)}{C.E}")
    logs = glob.glob(os.path.join(LOGS_DIR, "*"))
    if logs:
        for f in logs: os.remove(f)
        print(f"{C.G}[+] Удалено логов: {len(logs)}{C.E}")
    adb("shell pm trim-caches 999G"); print(f"{C.G}[+] Кэш Android очищен!{C.E}")
    input("\nНажми Enter...")

def backup_current_script():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(BACKUP_DIR, f"cyberdeck_backup_{timestamp}.py")
    try: shutil.copy(__file__, dest); print(f"\n{C.G}[+] Бэкап: backup/{os.path.basename(dest)}{C.E}")
    except Exception as e: print(f"\n{C.F}[!] Ошибка: {e}{C.E}")
    input("Нажми Enter...")

def get_battery():
    print(f"\n{C.CY}[*] Батарея...{C.E}")
    out = adb("shell dumpsys battery | grep -E 'level|status|temperature'")
    if out: print(f"{C.G}{out}{C.E}")
    input("Нажми Enter...")

# --- 🌡️ ТЕМПЕРАТУРА ---
def get_temperature():
    print(f"\n{C.CY}[*] Температура батареи...{C.E}")

    temp_c = None
    source = "dumpsys battery"

    out = adb("shell dumpsys battery")
    for line in out.split('\n'):
        line = line.strip()
        if line.startswith("temperature:"):
            try:
                raw = line.split(":", 1)[1].strip()
                temp_c = int(raw) / 10.0
                break
            except ValueError:
                pass

    if temp_c is None:
        source = "/sys/class/power_supply/battery/temp"
        raw = adb("shell cat /sys/class/power_supply/battery/temp").strip()
        try:
            temp_c = int(raw) / 10.0
        except ValueError:
            temp_c = None

    if temp_c is None:
        source = "/sys/class/thermal/thermal_zone0/temp"
        raw = adb("shell cat /sys/class/thermal/thermal_zone0/temp").strip()
        try:
            v = int(raw)
            temp_c = v / 1000.0 if v > 1000 else v / 10.0
        except ValueError:
            temp_c = None

    if temp_c is None:
        print(f"{C.F}[!] Не удалось получить температуру ни одним способом.{C.E}")
        input("Нажми Enter...")
        return

    print(f"{C.G}[+] Батарея: {C.BOLD}{temp_c:.1f}°C{C.E}")
    print(f"{C.W}[i] Источник: {source}{C.E}\n")

    if temp_c < 15:
        print(f"{C.B}[❄️]  Холодно — батарея может работать хуже.{C.E}")
    elif temp_c < 35:
        print(f"{C.G}[✅] Нормально — всё в порядке.{C.E}")
    elif temp_c < 45:
        print(f"{C.W}[⚠️]  Тепло — лучше не нагружать.{C.E}")
    elif temp_c < 55:
        print(f"{C.F}[🔥] ГОРЯЧО — сними чехол, не играй.{C.E}")
    else:
        print(f"{C.F}{C.BOLD}[💀] КРИТИЧНО — выключи и дай остыть!{C.E}")

    input("Нажми Enter...")

def save_logs():
    filename = f"logcat_{int(time.time())}.txt"
    filepath = os.path.join(LOGS_DIR, filename)
    print(f"\n{C.CY}[*] Собираю логи...{C.E}")
    logs = adb("logcat -d -v threadtime -t 1000")
    with open(filepath, "w", encoding="utf-8") as f: f.write(logs)
    print(f"{C.G}[+] Логи: logs/{filename}{C.E}")
    input("Нажми Enter...")

def take_screenshot():
    filename = f"screen_{int(time.time())}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    print(f"\n{C.CY}[*] Скриншот...{C.E}")
    adb("shell screencap -p /sdcard/tmp_cyber.png")
    adb(f"pull /sdcard/tmp_cyber.png \"{filepath}\"")
    adb("shell rm /sdcard/tmp_cyber.png")
    print(f"{C.G}[+] Сохранен: screenshots/{filename}{C.E}")
    input("Нажми Enter...")

def play_screamer():
    if not os.path.exists(SCREAMS_DIR): return
    files = [f for f in os.listdir(SCREAMS_DIR) if f.endswith('.mp3')]
    if not files: print(f"\n{C.F}[!] Нет MP3 в 'screams'!{C.E}"); input(); return
    file_to_play = random.choice(files)
    local_path = os.path.join(SCREAMS_DIR, file_to_play)
    remote_path = f"/sdcard/Download/{file_to_play}"
    print(f"\n{C.F}[!] СКРИМЕР: {file_to_play}{C.E}")
    adb(f"push \"{local_path}\" \"{remote_path}\"")
    for _ in range(15): adb("shell input keyevent 24")
    adb(f'shell am start -a android.intent.action.VIEW -d file://{remote_path} -t audio/mp3')
    print(f"{C.G}[+] Отработал!{C.E}"); input("Нажми Enter...")

def reboot_phone(mode="normal"):
    print(f"\n{C.F}[*] Перезагрузка ({mode})...{C.E}")
    if mode == "recovery": adb("reboot recovery")
    elif mode == "poweroff": adb("shell reboot -p")
    else: adb("reboot")
    sys.exit()

# --- МЕНЮ ---
def main():
    setup_folders()
    clear()
    print(f"{C.CY}{C.BOLD}")
    print("    ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ███████╗ ██████╗██╗  ██╗")
    print("   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝██║ ██╔╝")
    print("   ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ██║█████╗  ██║     █████╔╝ ")
    print("   ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║  ██║██╔══╝  ██║     ██╔═██╗ ")
    print("   ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██████╔╝███████╗╚██████╗██║  ██╗")
    print("    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝")
    print(f"          [ CYBERDECK v11.3 - CROSS-PLATFORM ]{C.E}")
    print(f"{C.W}[i] Корень: {BASE_DIR}{C.E}\n")

    if not check_connection():
        print(f"{C.F}[!] ОШИБКА: Телефон не подключен! Сделай adb connect.{C.E}"); sys.exit()

    print(f"{C.G}[+] Связь установлена.{C.E}")

    while True:
        print(f"\n{C.B}╔════════════════════════════════════════╗{C.E}")
        print(f"{C.CY}{C.BOLD}║ 1. 🖥️  NEOFETCH                        ║{C.E}")
        print(f"{C.B}║ 2. Инфо: Батарея                       ║{C.E}")
        print(f"{C.CY}║ 3. Шпион: Сохранить ЛОГИ АНДРОИДА      ║{C.E}")
        print(f"{C.CY}║ 4. Шпион: Сделать скриншот             ║{C.E}")
        print(f"{C.W}║ 5. Система: УНИВЕРСАЛЬНЫЙ ДЕБЛОАТ      ║{C.E}")
        print(f"{C.F}║ 6. Пранк: АУДИО-СКРИМЕР                ║{C.E}")
        print(f"{C.F}║ 7. Питание: Выключение                 ║{C.E}")
        print(f"{C.F}║ 8. Питание: Recovery                   ║{C.E}")
        print(f"{C.H}╠════════════════════════════════════════╣{C.E}")
        print(f"{C.H}║ 9. 🚀 ЗАПУСТИТЬ ALL-IN-ONE (Пранки)    ║{C.E}")
        print(f"{C.H}║ 10. 💾 СДЕЛАТЬ БЭКАП ГЛАВНОГО СКРИПТА  ║{C.E}")
        print(f"{C.F}{C.BOLD}║ 11. 🧹 ОЧИСТИТЬ ВЕСЬ МУСОР (CLEANER)   ║{C.E}")
        print(f"{C.CY}{C.BOLD}║ 12. 📁 ВСТРОЕННЫЙ ПРОВОДНИК            ║{C.E}")
        print(f"{C.F}║ 13. 📦 МЕНЕДЖЕР ПРИЛОЖЕНИЙ (УДАЛЕНИЕ)  ║{C.E}")
        print(f"{C.CY}{C.BOLD}║ 14. 🌡️  ИНФО: ТЕМПЕРАТУРА БАТАРЕИ       ║{C.E}")
        print(f"{C.B}╚════════════════════════════════════════╝{C.E}")
        print(f"{C.F} 0. Выход{C.E}")

        choice = input(f"\n{C.BOLD}root@cyberdeck:~# {C.E}")

        if choice == '1': launch_script("neofetch.py")
        elif choice == '2': get_battery()
        elif choice == '3': save_logs()
        elif choice == '4': take_screenshot()
        elif choice == '5': debloat()
        elif choice == '6': play_screamer()
        elif choice == '7': reboot_phone("poweroff")
        elif choice == '8': reboot_phone("recovery")
        elif choice == '9': launch_script("all_in_one.py")
        elif choice == '10': backup_current_script()
        elif choice == '11': cleaner()
        elif choice == '12': file_explorer()
        elif choice == '13': launch_script("app_manager.py")
        elif choice == '14': get_temperature()
        elif choice == '0':
            print(f"\n{C.F}[!] Отключение...{C.E}")
            break
        else:
            print(f"{C.F}[!] Неизвестная команда.{C.E}")

if __name__ == "__main__":
    main()
