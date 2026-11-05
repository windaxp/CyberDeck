import subprocess
import sys

def adb(cmd):
    return subprocess.run(f"adb {cmd}", shell=True, capture_output=True, text=True).stdout

def main():
    print("=== 🔊 ТЕКСТ В ГОЛОС ===")
    text = input("Введи текст, который скажет телефон: ")
    
    # Команда для синтеза речи (работает на Android 11+)
    print(f"[*] Телефон говорит: {text}")
    res = adb(f'shell cmd text-to-speech speak "{text}"')
    
    if not res or "Exception" not in res:
        print("[+] Команда отправлена!")
    else:
        print("[-] Ошибка. Возможно, на телефоне нет движка Google TTS.")
        
    input("Нажми Enter...")

if __name__ == "__main__":
    main()
