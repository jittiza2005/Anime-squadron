import pyautogui as pag
import time

while True:
    x, y = pag.position()
    color = pag.pixel(x, y)

    print(f"X: {x} Y: {y} RGB: {color}")

    time.sleep(0.5)