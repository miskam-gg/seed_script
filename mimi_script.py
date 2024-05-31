import pyautogui
import time

#Координаты кнопок
print("Move the mouse to the desired position on the screen.")
time.sleep(5)

x, y = pyautogui.position()
print(f"Current mouse position: x={x}, y={y}")
