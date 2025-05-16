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

# @data_bp.route('/receive_gsr_data', methods=['POST'])
# def receive_gsr_data():
#     data = request.json
#     gsr_value = data.get('gsr_value')
#     if gsr_value is None:
#         return jsonify({'status': 'error', 'message': 'No se recibió valor GSR'}), 400

#     # Aquí puedes guardar el valor en la base de datos, en memoria, o como necesites
#     # Por ejemplo, podrías guardar en una variable global o en Redis para mostrar en el dashboard

#     print(f"Valor GSR recibido: {gsr_value}")
#     # TODO: Guardar o procesar el dato como necesites

#     return jsonify({'status': 'success', 'message': 'Dato recibido correctamente'})

latest_gsr_values = []

@data_bp.route('/receive_gsr_data', methods=['POST'])
def receive_gsr_data():
    data = request.json
    gsr_value = data.get('gsr_value')
    if gsr_value is None:
        return jsonify({'status': 'error', 'message': 'No se recibió valor GSR'}), 400

    latest_gsr_values.append(gsr_value)
    if len(latest_gsr_values) > 15:
        latest_gsr_values.pop(0)

    print(f"Valor GSR recibido: {gsr_value}")
    return jsonify({'status': 'success', 'message': 'Dato recibido correctamente'})

@data_bp.route('/latest_gsr', methods=['GET'])
def latest_gsr():
    return jsonify({'gsr_values': latest_gsr_values})