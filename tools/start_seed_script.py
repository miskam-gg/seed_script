import json
import sys
import pyautogui
import time
import subprocess
import logging
import pyperclip
import os
import requests

pyautogui.FAILSAFE = False

# Настройка логирования в консоль и в поток stdout
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_and_wait(message, wait_time):
    logging.info(message)
    time.sleep(wait_time)

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def perform_clicks(resolution):
    coordinates = {
        "HD_resolution": [
            (956, 88), (630, 177), (391, 253), (1595, 927)
        ],
        "2K_resolution": [
            (1274, 117), (840, 236), (521, 337), (2126, 1236)
        ],
        "LOW_resolution": [
            (637, 58), (420, 118), (260, 168), (1063, 618)
        ]
    }
    clicks = coordinates.get(resolution)
    if clicks:
        for (x, y) in clicks:
            pyautogui.doubleClick(x, y)
            time.sleep(0.5)

def enter_server_name_via_clipboard(text):
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    entered_text = pyperclip.paste()
    logging.info(f"Entered text: '{entered_text}'")
    return entered_text.strip() == text.strip()

def get_player_count(server_id):
    url = f"https://api.battlemetrics.com/servers/{server_id}"
    response = requests.get(url)
    data = response.json()
    return data['data']['attributes']['players']

def switch_server(server_name, first_run=False):
    if not first_run:
        pyautogui.press('esc')
        log_and_wait("Pressed ESC to exit current server", 10)
    else:
        pyautogui.moveTo(x=960, y=540)
        pyautogui.click()
        log_and_wait("Clicked in the center of the screen", 5)
    log_and_wait("Navigating to Servers menu", 10)
    pyautogui.moveTo(x=956, y=88)
    pyautogui.click()
    pyautogui.click()
    log_and_wait("Double clicked on Servers menu", 10)
    pyautogui.moveTo(x=630, y=177)
    pyautogui.click()
    pyautogui.doubleClick()
    pyautogui.doubleClick()
    log_and_wait("Double clicked on search field to activate it", 10)
    logging.info("Entering server name in search field")
    if not enter_server_name_via_clipboard(server_name):
        log_and_wait("Retrying to enter server name", 10)
        enter_server_name_via_clipboard(server_name)
    log_and_wait("Typed server name in search field", 10)
    pyautogui.press('enter')
    log_and_wait("Pressed Enter to search for server", 10)
    pyautogui.moveTo(x=391, y=253)
    pyautogui.click()
    log_and_wait("Clicked to the server", 10)
    pyautogui.moveTo(x=1595, y=927)
    pyautogui.doubleClick()
    log_and_wait("Clicked to join to the server", 30)
    logging.info("Successfully connected to the server")

def shutdown():
    logging.info("Simulating shutdown... System would now shutdown.")
    log_and_wait("Shutdown simulated. Exiting script.", 10)

def launch_game(game_path):
    try:
        logging.info(f"Launching Squad game from path: {game_path}")
        if not os.path.exists(game_path):
            raise FileNotFoundError(f"File not found: {game_path}")
        subprocess.Popen([game_path])
        log_and_wait("Game launched, waiting for it to load", 60)
        switch_server("[RU] [RFS] Russian Freedom Server", first_run=True)
        monitor_servers()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def monitor_servers():
    servers = [
        ("26737505", "[RU] [RFS: INV] Russian Freedom Server"),
        ("27255969", "[RU] [RFS: #2] Russian Freedom Server"),
        ("27649562", "[RU] [RFS] Russian Freedom Server")
    ]
    for server_id, server_name in servers:
        while True:
            players_count = get_player_count(server_id)
            logging.info(f"Current player count on {server_name}: {players_count}")
            if players_count > 80:
                logging.info(f"Switching to the next server: {server_name}")
                switch_server(server_name)
                break
            time.sleep(600)
    shutdown()

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        config_path = os.path.join(sys._MEIPASS, 'seed_config.json')
    else:
        # Running in a normal Python environment
        if len(sys.argv) < 2:
            logging.error("No configuration file path provided.")
            sys.exit(1)
        config_path = sys.argv[1]

    config = load_config(config_path)
    perform_clicks(config['resolution'])
    launch_game(config['squadgame_path'])
