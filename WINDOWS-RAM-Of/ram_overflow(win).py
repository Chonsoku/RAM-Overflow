import time, random, os, platform, psutil, signal, sys, tkinter as tk
from tkinter import messagebox

rand_num = random.randint(1, 3)
memory_hog = []
os_name = platform.system()
blocked_signals = False
RESERVED_GB = 2       # Резервное ОЗУ

root = tk.Tk()
root.withdraw()


def system_reboot_or_shutdown():
    if os_name == "Windows":
        os.system("shutdown /s /t 0")
    else:
        print(f"Unknown OS: {os_name}.")
        time.sleep(1)
        print("Attempt to execute a command based on a Unix-like system pattern...")
        time.sleep(3)
        os.system("sudo shutdown -P now || sudo reboot || reboot")


def random_event():
    global blocked_signals, added_mb, total_used_gb
    if rand_num == 1:
        messagebox.showerror("CRITICAL ERROR", "RAM OVERFLOW. Program crash!")
        os._exit(1)
    elif rand_num == 2:
        messagebox.showwarning("SYSTEM ERROR", f"RAM OVERFLOW. The operating system: {os_name} - has crashed!")
        blocked_signals = True
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        time.sleep(4.2)
        system_reboot_or_shutdown()
        os._exit(0)
    else:
        print("CONTINUING RAM FILLING | Filling RAM to crash...")
        blocked_signals = True                                          # Блокировка SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while True:                                                     # Продолжение переполения ОЗУ
            garbage = bytes(1024 * 1024 * 100)
            memory_hog.append(garbage)
            mem = psutil.virtual_memory()
            print(f"Added: +{added_mb}MB | Total allocated: {total_used_gb:.1f}GB | RAM used: {mem.percent:.0f}%", end='\r')
            time.sleep(0.01)
        

def main():
    global added_mb, total_used_gb
    total_used_gb = 0
    try:
        while True:
            mem = psutil.virtual_memory()
            available_bytes = mem.available
            process = psutil.Process()                                  # Текущий процесс
            
            added_mb = 100
            total_used_gb += added_mb / 1024
            print(f"Added: +{added_mb}MB | Total allocated: {total_used_gb:.1f}GB | RAM used: {process.memory_info().rss/1024**3:.1f}GB", end='\r')
                
            if available_bytes < RESERVED_GB * 1024**3:
                print(f"\nTRIGGER! rand_num={rand_num}")
                random_event()
                
            garbage = bytes(1024 * 1024 * 100)
            memory_hog.append(garbage)
    except MemoryError:
        print(f"\nTRIGGER! rand_num={rand_num}")
        random_event()
    except KeyboardInterrupt:
        print("\n...exiting programs -> |.|")
        os._exit(0)

if __name__ == "__main__":
    main()
