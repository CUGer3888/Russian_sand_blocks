"""
goal: 随机按下方向键左键或右键
"""
import random
import time

import pyautogui
while True:
    pyautogui.keyDown(random.choice(['left', 'right']))
    pyautogui.keyUp(random.choice(['left', 'right']))
    time.sleep(0.01)