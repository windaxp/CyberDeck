import subprocess
import sys
import os

class C:
    G = '\033[92m'
    W = '\033[93m'
    F = '\033[91m'
    CY = '\033[96m'
    E = '\033[0m'

def adb(cmd):
    return subprocess.run(f"adb {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    print("=== 📦 МЕНЕДЖЕР ПРИЛОЖЕНИЙ ===")
    print("[*] Получаю список установленных приложений...")
    
    # Получаем список сторонних приложений (не системных)
    out = adb("shell pm list packages -3")
    pkgs = [line.replace("package:", "") for line in out.split('\n') if line]
    pkgs.sort()

    if not pkgs:
        print("[-] Нет установленных приложений.")
        sys.exit()

    for i, p in enumerate(pkgs, 1):
        print(f"{C.CY}{i:03d}{C.E}. {p}")

    print(f"\n{C.W}Введи номер приложения для УДАЛЕНИЯ (или 0 для выхода){C.E}")
    choice = input("> ")

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(pkgs):
            target = pkgs[idx]
            confirm = input(f"{C.F}Удалить {target}? (y/n): {C.E}")
            if confirm.lower() == 'y':
                res = adb(f"shell pm uninstall --user 0 {target}")
                print(f"{C.G if 'Success' in res else C.F}{res}{C.E}")
        elif choice != '0':
            print("[-] Неверный номер.")
    input("Нажми Enter...")

if __name__ == "__main__":
    main()
