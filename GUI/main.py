import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import json
import os
import requests
import sys
import subprocess
import ctypes
import time
import threading
import logging
import pygame


# Добавьте путь к каталогу 'tools' в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
from tools import search_squadgame, shutdown, start_seed_script, switch_layout
from tools.search_squadgame import find_squad_exe
# Инициализация Pygame для воспроизведения звука
pygame.mixer.init()

# Глобальный словарь с идентификаторами серверов
SERVER_IDS = {
    "Main": "26737505",
    "Mod": "27909506",
    "Inv": "27255969"
}

# Настройка логирования для отправки в Text виджет
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.see(tk.END)
        self.text_widget.after(0, append)

def get_keyboard_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetKeyboardLayout = user32.GetKeyboardLayout
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetForegroundWindow = user32.GetForegroundWindow

    hwnd = GetForegroundWindow()
    thread_id = GetWindowThreadProcessId(hwnd, 0)
    layout_id = GetKeyboardLayout(thread_id)

    language_id = layout_id & 0xFFFF

    layout_dict = {
        0x409: 'EN',  # English
        0x419: 'RU'  # Russian
    }

    return layout_dict.get(language_id, 'Unknown')

def is_caps_lock_on():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    VK_CAPITAL = 0x14
    return user32.GetKeyState(VK_CAPITAL) & 0x0001 != 0

def toggle_caps_lock():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    VK_CAPITAL = 0x14
    user32.keybd_event(VK_CAPITAL, 0, 0, 0)
    user32.keybd_event(VK_CAPITAL, 0, 2, 0)

def switch_to_english_layout():
    if is_caps_lock_on():
        toggle_caps_lock()
        time.sleep(0.5)

    current_layout = get_keyboard_layout()
    if current_layout != 'EN':
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        VK_MENU = 0x12
        VK_SHIFT = 0x10
        user32.keybd_event(VK_MENU, 0, 0, 0)
        user32.keybd_event(VK_SHIFT, 0, 0, 0)
        user32.keybd_event(VK_SHIFT, 0, 2, 0)
        user32.keybd_event(VK_MENU, 0, 2, 0)
        time.sleep(1)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SEED RFS")
        self.geometry("800x600")

        icon_path = os.path.join(os.path.dirname(__file__), 'RFS.png')
        if os.path.exists(icon_path):
            self.iconphoto(False, tk.PhotoImage(file=icon_path))

        self.config_file = 'config.txt'
        self.seed_config_file = 'seed_config.json'
        self.load_config()

        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        # Create frames for each tab
        self.menu_frame = ttk.Frame(self.notebook)
        self.logs_frame = ttk.Frame(self.notebook)
        self.about_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.menu_frame, text='Menu')
        self.notebook.add(self.logs_frame, text='Logs')
        self.notebook.add(self.about_frame, text='About')

        # Populate the frames with content
        self.create_menu_tab()
        self.create_logs_tab()
        self.create_about_tab()

        # Start updating player counts
        self.update_player_counts()
        self.after(1000, self.update_keyboard_layout)  # Call this after all widgets are created

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                try:
                    self.config_data = json.load(f)
                except json.JSONDecodeError:
                    self.config_data = self.default_config()
        else:
            self.config_data = self.default_config()

    def default_config(self):
        return {
            'squadgame_path': '',
            'resolution': 'HD_resolution',
            'servers': {
                'main': '',
                'mod': '',
                'inv': ''
            }
        }

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config_data, f, indent=4)

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.squadgame_path_var.set(filepath)
            self.config_data['squadgame_path'] = filepath
            self.save_config()

    def search_file(self):
        squad_exe_path = find_squad_exe()
        if squad_exe_path:
            self.squadgame_path_var.set(squad_exe_path)
            self.config_data['squadgame_path'] = squad_exe_path
            self.save_config()
            self.clipboard_clear()
            self.clipboard_append(squad_exe_path)
            messagebox.showinfo("File Found", f"SquadGame.exe found at: {squad_exe_path}\nPath copied to clipboard.")
        else:
            messagebox.showwarning("File Not Found", "SquadGame.exe not found.")

    def set_resolution(self, resolution):
        self.config_data['resolution'] = resolution
        self.save_config()

    def switch_layout(self):
        switch_to_english_layout()
        self.update_keyboard_layout()

    def update_keyboard_layout(self):
        current_layout = get_keyboard_layout()
        self.layout_var.set(f"Current layout: {current_layout}")
        if current_layout == 'EN':
            self.warning_label.config(text="English layout selected. You can start the script.", foreground="green")
        else:
            self.warning_label.config(text="Make sure to select English before starting the script", foreground="red")
        self.after(1000, self.update_keyboard_layout)

    def create_menu_tab(self):
        # Squadgame path
        ttk.Label(self.menu_frame, text="Squadgame.exe Path:").pack(anchor='w', padx=10, pady=5)
        self.squadgame_path_var = tk.StringVar(value=self.config_data['squadgame_path'])
        entry = ttk.Entry(self.menu_frame, textvariable=self.squadgame_path_var, width=70)
        entry.pack(anchor='w', padx=10, pady=5)

        button_frame = ttk.Frame(self.menu_frame)
        button_frame.pack(anchor='w', padx=10, pady=5)

        ttk.Button(button_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Search", command=self.search_file).pack(side=tk.LEFT)

        # Resolution selection
        ttk.Label(self.menu_frame, text="Current Resolution:").pack(anchor='w', padx=10, pady=5)
        resolutions = {
            "HD (1920x1080)": "HD_resolution",
            "2K (2560x1440)": "2K_resolution",
            "Low (1280x720)": "LOW_resolution"
        }
        self.resolution_var = tk.StringVar(value=self.config_data['resolution'])
        for text, value in resolutions.items():
            ttk.Radiobutton(self.menu_frame, text=text, variable=self.resolution_var, value=value,
                            command=lambda v=value: self.set_resolution(v)).pack(anchor='w', padx=10, pady=2)

        # Server player counts
        ttk.Label(self.menu_frame, text="Server Player Counts:").pack(anchor='w', padx=10, pady=5)
        self.server_counts = {}
        for server in SERVER_IDS.keys():
            count_frame = ttk.Frame(self.menu_frame)
            count_frame.pack(anchor='w', padx=10, pady=2, fill='x')
            count_var = tk.StringVar(value="Fetching...")
            self.server_counts[server] = count_var
            ttk.Label(count_frame, text=f"{server} Server:").pack(side=tk.LEFT, padx=10)
            ttk.Label(count_frame, textvariable=count_var).pack(side=tk.LEFT, padx=10)
            ttk.Button(count_frame, text="Refresh", command=lambda s=server: self.fetch_player_count(s, SERVER_IDS[s])).pack(side=tk.LEFT, padx=10)

        # Current layout and switch button
        self.layout_var = tk.StringVar()
        layout_frame = ttk.Frame(self.menu_frame)
        layout_frame.pack(anchor='w', padx=10, pady=5)
        ttk.Label(layout_frame, textvariable=self.layout_var).pack(side=tk.LEFT, padx=10)
        ttk.Button(layout_frame, text="Switch to English", command=self.switch_layout).pack(side=tk.LEFT)

        # Add a warning label
        self.warning_label = ttk.Label(self.menu_frame, text="Make sure to select English before starting the script", foreground="red")
        self.warning_label.pack(anchor='w', padx=10, pady=5)

        # Start seed script button
        ttk.Button(self.menu_frame, text="Start Seed Script", command=self.start_seed_script).pack(pady=10)
        # Create seed EXE button
        ttk.Button(self.menu_frame, text="Create Seed EXE", command=self.create_seed_exe).pack(pady=10)

    def fetch_player_count(self, server, server_id):
        url = f"https://api.battlemetrics.com/servers/{server_id}"
        try:
            response = requests.get(url)
            data = response.json()
            player_count = data['data']['attributes']['players']
            self.server_counts[server].set(f"{player_count} players")
        except Exception as e:
            self.server_counts[server].set(f"Error: {e}")

    def update_player_counts(self):
        for server, server_id in SERVER_IDS.items():
            self.fetch_player_count(server, server_id)
        self.after(600000, self.update_player_counts)

    def start_seed_script(self):
        seed_config = {
            'squadgame_path': self.config_data['squadgame_path'],
            'resolution': self.config_data['resolution'],
        }
        with open(self.seed_config_file, 'w') as f:
            json.dump(seed_config, f)

        script_path = os.path.join(os.path.dirname(__file__), '../tools/start_seed_script.py')
        process = subprocess.Popen([sys.executable, script_path, self.seed_config_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        thread = threading.Thread(target=self.log_output, args=(process,))
        thread.start()

    def log_output(self, process):
        for line in iter(process.stdout.readline, ''):
            self.logs_text.insert(tk.END, line)
            self.logs_text.see(tk.END)
        process.stdout.close()
        process.wait()

    def create_seed_exe(self):
        seed_config = {
            'squadgame_path': self.config_data['squadgame_path'],
            'resolution': self.config_data['resolution'],
        }
        with open(self.seed_config_file, 'w') as f:
            json.dump(seed_config, f)

        save_path = filedialog.asksaveasfilename(defaultextension=".exe", filetypes=[("Executable files", "*.exe")])
        if save_path:
            script_path = os.path.join(os.path.dirname(__file__), '../tools/start_seed_script.py')
            command = [
                'pyinstaller',
                '--onefile',
                '--add-data', f'{self.seed_config_file};.',
                '--name', 'seed_script',
                script_path,
                '--distpath', os.path.dirname(save_path)
            ]
            subprocess.run(command)
            exe_file = os.path.join(os.path.dirname(save_path), 'seed_script.exe')
            if os.path.exists(exe_file):
                os.rename(exe_file, save_path)
            messagebox.showinfo("Success", f"Executable created at: {save_path}")

    def create_logs_tab(self):
        self.logs_text = scrolledtext.ScrolledText(self.logs_frame, wrap=tk.WORD, width=100, height=30)
        self.logs_text.pack(pady=10, padx=10)

    def play_sound(self):
        sound_path = os.path.join(os.path.dirname(__file__), 'bolt.mp3')
        if os.path.exists(sound_path):
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        else:
            messagebox.showerror("Error", "Sound file not found.")

    def create_about_tab(self):
        label = ttk.Label(self.about_frame, text="ОБЯЗАТЕЛЬНО ПЕРЕД ЗАПУСКОМ ВЫСТАВИТЬ АНГЛИЙСКИЙ ЯЗЫК!!!\nЛУЧШЕ ВЫСТАВИТЬ ЕГО ОСНОВНЫМ В СИСТЕМЕ.\nVersion 0.1337\nby axaxaB")
        label.pack(pady=20, padx=20)

        # Создание маленькой кнопки для проигрывания звука
        bolt_button = tk.Button(self.about_frame, text="❤", width=2, height=1, command=self.play_sound)
        bolt_button.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # Размещаем кнопку в правом нижнем углу

if __name__ == "__main__":
    app = App()
    app.mainloop()
