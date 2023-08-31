# PS/2 mouse and keyboard have to be connect to your PC
# Your PC must support intel8042

from autoguiwinio import initautogui
from autoguiwinio import auto

InitWinIo = initautogui.InitWinIo
ShutDownWinIo = initautogui.ShutDownWinIo
KeyDown = auto.KeyDown
KeyUp = auto.KeyUp
KeyCode = auto.KeyCode
PressMouseKey = auto.PressMouseKey