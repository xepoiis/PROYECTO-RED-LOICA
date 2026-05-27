import http.server
import socketserver
import socket
import os

class CaptivePortalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Sobrescribe el método GET para servir siempre el index.html"""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # Lee el archivo index.html de la misma carpeta
        ruta_html = os.path.join(os.path.dirname(__file__), 'index.html')
        try:
            with open(ruta_html, 'rb') as file:
                self.wfile.write(file.read())
        except FileNotFoundError:
            self.wfile.write(b"<h1>Error 404: Archivo index.html no encontrado en la carpeta.</h1>")

def obtener_ip_local():
    """Obtiene la dirección IP local de la máquina"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def iniciar_servidor(puerto=80):
    """Inicia el servidor TCP Multihilo en el puerto especificado"""
    # ¡AQUÍ ESTÁ LA MAGIA! ThreadingTCPServer permite múltiples conexiones simultáneas
    httpd = socketserver.ThreadingTCPServer(("", puerto), CaptivePortalHandler)
    print(f"[LOG] Servidor Mesh MULTIHILO activo. Escuchando peticiones en el puerto {puerto}...")
    httpd.serve_forever()