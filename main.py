import pyautogui
import time
import subprocess
import logging
from datetime import datetime

pyautogui.FAILSAFE = False

# Настройка логирования в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_and_wait(message, wait_time):
    logging.info(message)
    time.sleep(wait_time)


def wait_until(target_hour, target_minute):
    while True:
        now = datetime.now()
        if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_minute):
            logging.info("Target time reached or passed. Starting main script...")
            break
        else:
            logging.info(f"Waiting for {target_hour:02}:{target_minute:02}. Current time is {now.hour:02}:{now.minute:02}")
            time.sleep(60)  # Проверять время каждую минуту


def launch_game():
    try:
        # Запуск игры Squad
        logging.info("Launching Squad game")
        subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\Squad\SquadGame.exe"])  # Убедитесь, что путь к файлу правильный
        log_and_wait("Game launched, waiting for it to load", 60)

        # Переход в меню Servers
        pyautogui.click(x=956, y=88)  # Координаты кнопки Servers (поменяйте на реальные координаты)
        log_and_wait("Clicked on Servers menu", 5)

        # Поиск сервера
        pyautogui.click(x=630, y=177)  # Координаты поля поиска (поменяйте на реальные координаты)
        pyautogui.write("[RU] [RFS] Russian Freedom Server")
        log_and_wait("Writed on Servers menu", 10)
        pyautogui.press('enter')  # Нажатие клавиши Enter для поиска сервера
        log_and_wait("Searched for [RU] [RFS] Russian Freedom Server", 2)

        # Выбор сервера
        pyautogui.click(x=391, y=253)  # Координаты сервера в списке (поменяйте на реальные координаты)
        log_and_wait("Selected the server from the list", 5)

        # Подключение к серверу
        pyautogui.click(x=1654, y=930)  # Координаты кнопки подключения (поменяйте на реальные координаты)
        log_and_wait("Clicked to connect to the server", 60)
        logging.info("Successfully connected to the server")

        # Запуск скрипта player_count.py
        logging.info("Launching player_count.py script")
        subprocess.Popen(["python", r"C:\Users\Max\PycharmProjects\script_squad\player_count.py"])
        logging.info("player_count.py script launched")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    logging.info("Script started at: {}".format(datetime.now()))
    wait_until(4, 5)  # Ждать до 04:05
    launch_game()
