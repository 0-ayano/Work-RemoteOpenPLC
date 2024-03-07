import time
from serial.tools import list_ports
from pymodbus.client import ModbusSerialClient as ModbusClient

# ポート番号の自動取得
device_port = []
check_list = ["Arduino", "Raspberry", "ESP32"]
for info in list_ports.comports():
    for item in check_list:
        if item in info.description:
            device_port.append(info.device)

# modbus通信の用意
print(f"Arduinoと繋がっているCOMポート : {device_port[0]}")
client = ModbusClient(method = "rtu", port=device_port[0], baudrate= 115200, timeout=0.1)
client.connect()

time.sleep(1.6)

# coilの状態確認
rr = client.read_coils(address=0, count=20, slave=1)
print(rr.bits)
"""
client.write_coils(address=4, values=1, slave=1)
rr = client.read_coils(address=0, count=4, slave=1)
print(rr.bits)
"""

# registerの状態確認
rr = client.read_holding_registers(address=0, count=20, slave=1)
print(rr.registers)

client.close()