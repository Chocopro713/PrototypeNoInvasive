from flask import Blueprint, jsonify, request
import serial.tools.list_ports
import serial
import time
import re

data_bp = Blueprint('data', __name__)

# @data_bp.route('/available_ports', methods=['GET'])
# def available_ports():
#     ports = [port.description for port in serial.tools.list_ports.comports()]
#     print(f"Puertos disponibles: {ports}")
#     return jsonify({"ports": ports})

@data_bp.route('/available_ports', methods=['GET'])
def available_ports():
    ports = [port.description for port in serial.tools.list_ports.comports()]
    if not ports:
        print("No se encontraron puertos disponibles.")
        return jsonify({"ports": [], "message": "No se encontraron puertos disponibles."}), 200
    print(f"Puertos disponibles: {ports}")
    return jsonify({"ports": ports})

def extract_port_from_description(description):
    # Intentar extraer el puerto en formato COMx (Windows)
    match = re.search(r'\((COM\d+)\)', description)
    if match:
        return match.group(1)
    
    # Intentar extraer el puerto en formato numérico (e.g., 9025)
    match = re.search(r'\((\d+)\)', description)
    if match:
        return match.group(1)
    
    # Si no se encuentra un puerto válido, devolver None
    return None

# def open_serial_port(port):
#     try:
#         ser = serial.Serial(port, 9600, timeout=5)
#         return ser
#     except serial.SerialException as e:
#         print(f"Error al abrir el puerto {port}: {e}")
#         return None
    
def open_serial_port(port):
    try:
        print(f"Intentando abrir el puerto: {port}")
        ser = serial.Serial(port, baudrate=9600, timeout=5)
        print(f"Puerto {port} abierto correctamente.")
        return ser
    except serial.SerialException as e:
        print(f"Error al abrir el puerto {port}: {e}")
        return None

@data_bp.route('/data_gsr', methods=['GET'])
def get_gsr_data():
    port = request.args.get('port')  # Recibir el nombre del puerto directamente
    if not port:
        return jsonify({"error": "No se especificó el puerto"}), 400

    print(f"Puerto recibido: {port}")
    try:
        ser = open_serial_port(port)
        print(f"Puerto abierto: {ser}")
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

# @data_bp.route('/get_port_name', methods=['POST'])
# def get_port_name():
#     data = request.json
#     usb_vendor_id = data.get('usbVendorId')
#     usb_product_id = data.get('usbProductId')

#     for port in serial.tools.list_ports.comports():
#         if port.vid == usb_vendor_id and port.pid == usb_product_id:
#             return jsonify({"port_name": port.device})

#     return jsonify({"error": "No se encontró el puerto correspondiente"}), 404

@data_bp.route('/get_port_name', methods=['POST'])
def get_port_name():
    data = request.json
    usb_vendor_id = data.get('usbVendorId')
    usb_product_id = data.get('usbProductId')

    print(f"Buscando puerto con Vendor ID: {usb_vendor_id}, Product ID: {usb_product_id}")

    # Buscar el puerto que coincida con el usbVendorId y usbProductId
    for port in serial.tools.list_ports.comports():
        print(f"Revisando puerto: {port.device}, VID: {port.vid}, PID: {port.pid}")
        if port.vid == usb_vendor_id and port.pid == usb_product_id:
            return jsonify({"port_name": port.device})

    # Si no se encuentra una coincidencia, devolver todos los puertos disponibles
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if ports:
        return jsonify({"error": "No se encontró el puerto específico, pero estos están disponibles.", "available_ports": ports}), 404

    return jsonify({"error": "No se encontraron puertos disponibles"}), 404