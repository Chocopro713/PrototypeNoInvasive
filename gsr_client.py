# gsr_client.py
import serial
import time
import requests

SERIAL_PORT = 'COM5'  # Cambia esto según el puerto de tu Arduino
BAUDRATE = 9600
RENDER_API_URL = 'https://prototypenoinvasive.onrender.com/receive_gsr_data'  # Cambia esto por tu dominio real

def read_gsr():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
        time.sleep(2)
        if ser.in_waiting:
            value = ser.readline().decode('utf-8').strip()
            ser.close()
            return int(value)
        ser.close()
    except Exception as e:
        print("Error leyendo el puerto serial:", e)
    return None

def main():
    while True:
        gsr_value = read_gsr()
        if gsr_value is not None:
            print("Enviando valor GSR:", gsr_value)
            try:
                response = requests.post(RENDER_API_URL, json={'gsr_value': gsr_value})
                print("Respuesta del servidor:", response.text)
            except Exception as e:
                print("Error enviando datos:", e)
        time.sleep(1)  # Espera 1 segundo entre lecturas

if __name__ == '__main__':
    main()