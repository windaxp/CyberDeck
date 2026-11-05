import os
import subprocess
import sys
import time
import random
import shutil
import glob

# --- ЖЕСТКИЕ ПУТИ ---
BASE_DIR = "/sdcard/Download/CyberDeck"
SCREAMS_DIR = os.path.join(BASE_DIR, "screams")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

def setup_folders():
    for folder in [BASE_DIR, SCREAMS_DIR, LOGS_DIR, SCREENSHOTS_DIR, SCRIPTS_DIR, BACKUP_DIR]:
        if not os.path.exists(folder):
            os.makedirs(folder)

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

# --- ФУНКЦИИ ЗАПУСКА СКРИПТОВ ИЗ ПАПКИ SCRIPTS ---
def launch_neofetch():
    script_path = os.path.join(SCRIPTS_DIR, "neofetch.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"\n{C.F}[!] Ошибка: Файл scripts/neofetch.py не найден!{C.E}")
        input("Нажми Enter...")

def launch_all_in_one():
    script_path = os.path.join(SCRIPTS_DIR, "all_in_one.py")
    if os.path.exists(script_path):
        print(f"\n{C.CY}[*] Запускаю ALL-IN-ONE...{C.E}")
        time.sleep(1)
        subprocess.run(["python", script_path])
    else:
        print(f"\n{C.F}[!] Ошибка: Файл scripts/all_in_one.py не найден!{C.E}")
        input("Нажми Enter...")

def launch_tts():
    script_path = os.path.join(SCRIPTS_DIR, "tts.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"\n{C.F}[!] Ошибка: Файл scripts/tts.py не найден!{C.E}")
        input("Нажми Enter...")

def launch_app_manager():
    script_path = os.path.join(SCRIPTS_DIR, "app_manager.py")
    if os.path.exists(script_path):
        subprocess.run(["python", script_path])
    else:
        print(f"\n{C.F}[!] Ошибка: Файл scripts/app_manager.py не найден!{C.E}")
        input("Нажми Enter...")

# --- ВСТРОЕННЫЙ ПРОВОДНИК ---
def file_explorer():
    current_dir = BASE_DIR
    while True:
        clear()
        print(f"{C.CY}{C.BOLD}=== 📁 ВСТРОЕННЫЙ ПРОВОДНИК ==={C.E}")
        print(f"{C.W}Текущая папка: {current_dir}{C.E}\n")
        
        try:
            items = os.listdir(current_dir)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(current_dir, x)), x.lower()))
        except PermissionError:
            print(f"{C.F}[!] Нет доступа к этой папке.{C.E}")
            input("Нажми Enter...")
            current_dir = BASE_DIR
            continue
            
        if not items:
            print(f"{C.W}Папка пуста.{C.E}")
            
        for i, item in enumerate(items, 1):
            path = os.path.join(current_dir, item)
            if os.path.isdir(path):
                print(f"  {C.B}[{i}] 📁 {item}/{C.E}")
            else:
                try:
                    size = os.path.getsize(path) / 1024
                    print(f"  {C.G}[{i}] 📄 {item} ({size:.1f} KB){C.E}")
                except OSError:
                    print(f"  {C.G}[{i}] 📄 {item}{C.E}")
                
        print(f"\n{C.W}Команды:{C.E}")
        print(f"  [номер] - зайти в папку")
        print(f"  {C.F}del [номер]{C.E} - удалить файл")
        print(f"  {C.CY}cd [путь]{C.E} - перейти по пути")
        print(f"  [0] - вернуться в главное меню")
        
        cmd = input(f"\n{C.BOLD}Проводник > {C.E}").strip().split()
        
        if not cmd: continue
        if cmd[0] == '0': break
        elif cmd[0].lower() == 'cd' and len(cmd) > 1:
            new_dir = " ".join(cmd[1:])
            if os.path.exists(new_dir) and os.path.isdir(new_dir): current_dir = new_dir
            else:
                print(f"{C.F}[!] Путь не найден.{C.E}")
                time.sleep(1)
        elif cmd[0].lower() == 'del' and len(cmd) > 1:
            try:
                idx = int(cmd[1]) - 1
                if 0 <= idx < len(items):
                    target = os.path.join(current_dir, items[idx])
                    if os.path.isdir(target): print(f"{C.F}[!] Это папка. Удалять нельзя.{C.E}")
                    else:
                        os.remove(target)
                        print(f"{C.G}[+] Файл {items[idx]} удален!{C.E}")
                else: print(f"{C.F}[!] Неверный номер.{C.E}")
            except ValueError: print(f"{C.F}[!] Ошибка ввода.{C.E}")
            time.sleep(1)
        elif cmd[0].isdigit():
            idx = int(cmd[0]) - 1
            if 0 <= idx < len(items):
                target = os.path.join(current_dir, items[idx])
                if os.path.isdir(target): current_dir = target
                else:
                    print(f"{C.W}[i] Это файл.{C.E}")
                    time.sleep(1)

# --- СИСТЕМНЫЕ ФУНКЦИИ ---
def cleaner():
    clear()
    print(f"{C.F}{C.BOLD}=== 🧹 СИСТЕМА ОЧИСТКИ CYBERDECK ==={C.E}\n")
    screens = glob.glob(os.path.join(SCREENSHOTS_DIR, "*"))
    if screens:
        for f in screens: os.remove(f)
        print(f"{C.G}[+] Удалено скриншотов: {len(screens)}{C.E}")
    else: print(f"{C.W}[i] Папка screenshots уже пуста.{C.E}")

    logs = glob.glob(os.path.join(LOGS_DIR, "*"))
    if logs:
        for f in logs: os.remove(f)
        print(f"{C.G}[+] Удалено файлов логов: {len(logs)}{C.E}")
    else: print(f"{C.W}[i] Папка logs уже пуста.{C.E}")

    print(f"\n{C.CY}[*] Отправляю команду на очистку кэша Android...{C.E}")
    adb("shell pm trim-caches 999G")
    print(f"{C.G}[+] Кэш системы очищен!{C.E}")
    input("\nНажми Enter...")

def backup_current_script():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_name = f"cyberdeck_backup_{timestamp}.py"
    dest = os.path.join(BACKUP_DIR, backup_name)
    try:
        shutil.copy(__file__, dest)
        print(f"\n{C.G}[+] Бэкап создан: backup/{backup_name}{C.E}")
    except Exception as e:
        print(f"\n{C.F}[!] Ошибка: {e}{C.E}")
    input("Нажми Enter...")

def get_battery():
    print(f"\n{C.CY}[*] Считываю данные батареи...{C.E}")
    out = adb("shell dumpsys battery | grep -E 'level|status|temperature'")
    if out: print(f"{C.G}{out}{C.E}")
    input("Нажми Enter...")

def save_logs():
    filename = f"logcat_{int(time.time())}.txt"
    filepath = os.path.join(LOGS_DIR, filename)
    print(f"\n{C.CY}[*] Собираю системные логи Android...{C.E}")
    logs = adb("logcat -d -v threadtime -t 1000")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(logs)
    print(f"{C.G}[+] Логи сохранены в: logs/{filename}{C.E}")
    input("Нажми Enter...")

def take_screenshot():
    filename = f"screen_{int(time.time())}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    print(f"\n{C.CY}[*] Делаю скриншот...{C.E}")
    adb("shell screencap -p /sdcard/tmp_cyber.png")
    adb(f"pull /sdcard/tmp_cyber.png {filepath}")
    adb("shell rm /sdcard/tmp_cyber.png")
    print(f"{C.G}[+] Скриншот сохранен: screenshots/{filename}{C.E}")
    input("Нажми Enter...")

def play_screamer():
    if not os.path.exists(SCREAMS_DIR): return
    files = [f for f in os.listdir(SCREAMS_DIR) if f.endswith('.mp3')]
    if not files:
        print(f"\n{C.F}[!] В папке 'screams' нет MP3 файлов!{C.E}")
        input("Нажми Enter...")
        return
    file_to_play = random.choice(files)
    local_path = os.path.join(SCREAMS_DIR, file_to_play)
    remote_path = f"/sdcard/Download/{file_to_play}"
    print(f"\n{C.F}{C.BOLD}[!] ЗАГРУЖАЮ СКРИМЕР: {file_to_play}{C.E}")
    adb(f"push \"{local_path}\" \"{remote_path}\"")
    for _ in range(15): adb("shell input keyevent 24")
    adb(f'shell am start -a android.intent.action.VIEW -d file://{remote_path} -t audio/mp3')
    print(f"{C.G}[+] Скример отработал!{C.E}")
    input("Нажми Enter...")

def debloat():
    print(f"\n{C.W}[*] Базовая чистка рекламы...{C.E}")
    pkgs = ["com.miui.msa.global", "com.miui.analytics", "com.xiaomi.mipicks", "com.miui.systemAdSolution"]
    for p in pkgs:
        res = adb(f"shell pm uninstall --user 0 {p}")
        print(f"  {C.G if 'Success' in res else C.W}{p}{C.E}")
    input("Нажми Enter...")

def reboot_phone(mode="normal"):
    print(f"\n{C.F}[*] Перезагрузка ({mode})...{C.E}")
    if mode == "recovery": adb("reboot recovery")
    elif mode == "fastboot": adb("reboot bootloader")
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
    print("   ╚██████╗   ██║   ██████╔╝███████╗██�  ██║██████╔╝███████╗╚██████╗██║  ██╗")
    print("    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝")
    print(f"              [ CYBERDECK v9.3 - MAIN HUB ]{C.E}\n")

    if not check_connection():
        print(f"{C.F}[!] ОШИБКА: Телефон не подключен! Сделай adb connect.{C.E}")
        sys.exit()
    
    print(f"{C.G}[+] Связь установлена.{C.E}")

    while True:
        print(f"\n{C.B}╔════════════════════════════════════════╗{C.E}")
        print(f"{C.CY}{C.BOLD}║ 1. 🖥️  NEOFETCH (Инфо о телефоне)      ║{C.E}")
        print(f"{C.B}║ 2. Инфо: Батарея                       ║{C.E}")
        print(f"{C.CY}║ 3. Шпион: Сохранить ЛОГИ АНДРОИДА      ║{C.E}")
        print(f"{C.CY}║ 4. Шпион: Сделать скриншот             ║{C.E}")
        print(f"{C.W}║ 5. Система: Деблоат (Удалить рекламу)  ║{C.E}")
        print(f"{C.F}║ 6. Пранк: АУДИО-СКРИМЕР                ║{C.E}")
        print(f"{C.F}║ 7. Питание: Выключение                 ║{C.E}")
        print(f"{C.F}║ 8. Питание: Recovery                   ║{C.E}")
        print(f"{C.H}╠════════════════════════════════════════╣{C.E}")
        print(f"{C.H}║ 9. 🚀 ЗАПУСТИТЬ ALL-IN-ONE (Пранки)    ║{C.E}")
        print(f"{C.H}║ 10. 💾 СДЕЛАТЬ БЭКАП ГЛАВНОГО СКРИПТА  ║{C.E}")
        print(f"{C.F}{C.BOLD}║ 11. 🧹 ОЧИСТИТЬ ВЕСЬ МУСОР (CLEANER)   ║{C.E}")
        print(f"{C.CY}{C.BOLD}║ 12. 📁 ВСТРОЕННЫЙ ПРОВОДНИК            ║{C.E}")
        print(f"{C.CY}║ 13. 🔊 ГОЛОС ИЗ ТЕЛЕФОНА (TTS)         ║{C.E}")
        print(f"{C.F}║ 14. 📦 МЕНЕДЖЕР ПРИЛОЖЕНИЙ (УДАЛЕНИЕ)  ║{C.E}")
        print(f"{C.B}╚════════════════════════════════════════╝{C.E}")
        print(f"{C.F} 0. Выход{C.E}")

        choice = input(f"\n{C.BOLD}root@cyberdeck:~# {C.E}")

        if choice == '1': launch_neofetch()
        elif choice == '2': get_battery()
        elif choice == '3': save_logs()
        elif choice == '4': take_screenshot()
        elif choice == '5': debloat()
        elif choice == '6': play_screamer()
        elif choice == '7': reboot_phone("poweroff")
        elif choice == '8': reboot_phone("recovery")
        elif choice == '9': launch_all_in_one()
        elif choice == '10': backup_current_script()
        elif choice == '11': cleaner()
        elif choice == '12': file_explorer()
        elif choice == '13': launch_tts()
        elif choice == '14': launch_app_manager()
        elif choice == '0':
            print(f"\n{C.F}[!] Отключение...{C.E}")
            break
        else:
            print(f"{C.F}[!] Неизвестная команда.{C.E}")

if __name__ == "__main__":
    main()
