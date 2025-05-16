import serial

try:
    ser = serial.Serial('COM5', 9600, timeout=2)
    print("Puerto abierto correctamente")
    ser.close()
except Exception as e:
    print("Error:", e)