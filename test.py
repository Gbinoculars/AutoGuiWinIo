import autoguiwinio
import time

dllRootPath = "dllRootPath"

if (autoguiwinio.InitWinIo(dllRootPath)!=0):
    print("error")
    exit()

while True:
    autoguiwinio.KeyDown(autoguiwinio.KeyCode.G)
    autoguiwinio.KeyUp(autoguiwinio.KeyCode.G)
    break

autoguiwinio.ShutDownWinIo()
