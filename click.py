import pyautogui
import time

while True:
    # перемещаем курсор в точку с координатами x=100, y=200
    pyautogui.moveTo(100, 200)
    # делаем клик мышью
    pyautogui.click()
    # ждем 2 секунды
    time.sleep(2)
