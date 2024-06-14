import subprocess
import time
import logging
import sys
import os

# Настройка логирования в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_switch_layout():
    result = subprocess.run([sys.executable, os.path.join(os.getcwd(), 'switch_layout.py')], capture_output=True, text=True)
    logging.info(f"Switch layout script stdout: {result.stdout}")
    logging.info(f"Switch layout script stderr: {result.stderr}")
    logging.info("Switch layout script completed")

def run_main_script():
    result = subprocess.run([sys.executable, os.path.join(os.getcwd(), 'first_script.py')], capture_output=True, text=True)
    logging.info(f"Main script stdout: {result.stdout}")
    logging.info(f"Main script stderr: {result.stderr}")
    logging.info("Main script completed")

def check_modules():
    try:
        import pyautogui
        import pyperclip
    except ImportError as e:
        logging.error(f"Module not found: {e}. Please install the required modules using 'pip install pyautogui pyperclip'")
        exit(1)

if __name__ == "__main__":
    logging.info("Master script started")
    check_modules()
    run_switch_layout()
    time.sleep(120)  # Задержка в 2 минуты после смены языка
    run_main_script()
    logging.info("Master script completed")
