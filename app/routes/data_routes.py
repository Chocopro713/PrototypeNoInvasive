from flask import Blueprint, jsonify, request
import serial.tools.list_ports
import serial
import time
import re

data_bp = Blueprint('data', __name__)

@data_bp.route('/available_ports', methods=['GET'])
def available_ports():
    ports = [port.description for port in serial.tools.list_ports.comports()]
    print(f"Puertos disponibles: {ports}")
    return jsonify({"ports": ports})

def extract_port_from_description(description):
    match = re.search(r'\((COM\d+)\)', description)
    if match:
        return match.group(1)
    return None

def open_serial_port(port):
    try:
        ser = serial.Serial(port, 9600, timeout=5)
        return ser
    except serial.SerialException as e:
        print(f"Error al abrir el puerto {port}: {e}")
        return None

@data_bp.route('/data_gsr', methods=['GET'])
def get_gsr_data():
    port_description = request.args.get('port')
    if not port_description:
        return jsonify({"error": "No se especificó el puerto"}), 400

    port = extract_port_from_description(port_description)
    if not port:
        return jsonify({"error": "Descripción del puerto inválida"}), 400

    try:
        ser = open_serial_port(port)
        if ser:
            start_time = time.time()
            readings = 0
            gsr_values = []
            while True:
                if time.time() - start_time > 15:  # Limitar a 15 segundos
                    break
                if readings >= 15:  # Limitar a 15 lecturas
                    break
                if ser.in_waiting:
                    gsr_value = ser.readline().decode('utf-8').strip()
                    print(f"Valor GSR: {gsr_value}")
                    gsr_values.append(int(gsr_value))
                    readings += 1
                else:
                    time.sleep(0.1)  # Esperar un poco antes de volver a verificar
            return jsonify({"gsr_values": gsr_values})
        else:
            return jsonify({"error": "No se pudo abrir el puerto serie"})
    except Exception as e:
        print(f"Excepción: {e}")
        return jsonify({"error": str(e)})
    finally:
        if ser:
            ser.close()