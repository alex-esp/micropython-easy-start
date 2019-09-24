esptool.py --port com4 chip_id

esptool.py --port com4  erase_flash

REM esptool.py --chip esp32 --port com4 --baud 460800 write_flash -z 0x00001000 ../esp32-20190823-v1.11-240.bin
esptool.py --port com4 --baud 460800 write_flash -z 0x00001000 esp32-20190823-v1.11-240.bin
