import pyautogui
import time
import subprocess
import logging
import pyperclip
import os

pyautogui.FAILSAFE = False

# Настройка логирования в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Функция для ожидания с логированием
def log_and_wait(message, wait_time):
    logging.info(message)
    time.sleep(wait_time)


# Функция для ввода текста по символу с задержками
def type_text_slowly(text, interval=0.2):
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(interval)


# Функция для ввода текста с проверкой
def enter_server_name(text):
    while True:
        pyautogui.click(x=630, y=177)  # Координаты поля поиска (поменяйте на реальные координаты)
        type_text_slowly(text)
        time.sleep(1)  # Подождите, чтобы текст ввелся
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        entered_text = pyperclip.paste()
        logging.info(f"Entered text: '{entered_text}'")
        if entered_text.strip() == text.strip():
            break
        else:
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            log_and_wait("Retrying to enter server name", 2)


# Функция для запуска игры и подключения к серверу
def launch_game():
    try:
        # Запуск игры Squad
        logging.info("Launching Squad game")
        subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\Squad\SquadGame.exe"])  # Убедитесь, что путь к файлу правильный
        log_and_wait("Game launched, waiting for it to load", 60)

        # Переход в меню Servers
        logging.info("Navigating to Servers menu")
        pyautogui.click(x=956, y=88)  # Координаты кнопки Servers (поменяйте на реальные координаты)
        log_and_wait("Clicked on Servers menu", 10)

        # Убедимся, что окно активно
        pyautogui.click(x=630, y=177)  # Координаты поля поиска (поменяйте на реальные координаты)
        log_and_wait("Clicked on search field to activate it", 5)

        # Поиск сервера
        logging.info("Entering server name in search field")
        server_name = "[RU] [RFS] Russian Freedom Server"
        enter_server_name(server_name)  # Ввод текста с проверкой
        log_and_wait("Typed server name in search field", 20)
        pyautogui.press('enter')
        log_and_wait("Pressed Enter to search for server", 25)

        # Выбор сервера
        logging.info("Selecting the server from the list")
        pyautogui.doubleClick(x=391, y=253)  # Координаты сервера в списке (поменяйте на реальные координаты)
        pyautogui.doubleClick(x=391, y=253)  # Координаты сервера в списке (поменяйте на реальные координаты)
        log_and_wait("Selected the server from the list", 5)
        logging.info("Successfully connected to the server")

    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    logging.info("Script started")
    launch_game()