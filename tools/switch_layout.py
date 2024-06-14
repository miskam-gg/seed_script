import ctypes
import time
import logging

# Настройка логирования в консоль
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_keyboard_layout():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    GetKeyboardLayout = user32.GetKeyboardLayout
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetForegroundWindow = user32.GetForegroundWindow

    hwnd = GetForegroundWindow()
    thread_id = GetWindowThreadProcessId(hwnd, 0)
    layout_id = GetKeyboardLayout(thread_id)

    # Layout id is a hex value, the lower 16 bits are the language ID
    language_id = layout_id & 0xFFFF

    # Predefined layout ids for common languages
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
        logging.info("Caps Lock is on. Turning it off...")
        toggle_caps_lock()
        # Wait a little for Caps Lock to toggle
        time.sleep(0.5)

    current_layout = get_keyboard_layout()
    logging.info(f"Current keyboard layout: {current_layout}")
    if current_layout != 'EN':
        logging.info("Switching to English layout...")
        # Use Alt+Shift to switch the keyboard layout
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        VK_MENU = 0x12
        VK_SHIFT = 0x10
        user32.keybd_event(VK_MENU, 0, 0, 0)
        user32.keybd_event(VK_SHIFT, 0, 0, 0)
        user32.keybd_event(VK_SHIFT, 0, 2, 0)
        user32.keybd_event(VK_MENU, 0, 2, 0)
        # Wait a little for the layout to switch
        time.sleep(1)
        # Verify the layout switched
        new_layout = get_keyboard_layout()
        logging.info(f"New keyboard layout: {new_layout}")
    else:
        logging.info("Already in English layout.")

if __name__ == "__main__":
    switch_to_english_layout()
    logging.info("Switch layout script completed")
