import tkinter as tk
from tkinter import messagebox
import threading
import server  # Importamos nuestro propio módulo

# Variable de control
servidor_activo = False

def validar_pin():
    global servidor_activo
    pin_ingresado = entry_pin.get()
    
    if pin_ingresado == "1234":
        lbl_status.config(text="✔ PIN CORRECTO. EMERGENCIA ACTIVADA.", fg="#2ecc71")
        entry_pin.config(state="disabled")
        btn_activar.config(state="disabled")
        
        # Iniciamos el servidor web en un hilo secundario para no congelar la ventana
        if not servidor_activo:
            hilo_servidor = threading.Thread(target=server.iniciar_servidor, daemon=True)
            hilo_servidor.start()
            servidor_activo = True
            
            ip = server.obtener_ip_local()
            mensaje = (
                "Alarma transmitida exitosamente a la red Mesh.\n\n"
                "Instrucciones para el simulacro:\n"
                "1. Conéctense a la red Wi-Fi compartida.\n"
                f"2. Abran el navegador y escriban: http://{ip}"
            )
            messagebox.showwarning("SISTEMA ACTIVO", mensaje)
    else:
        lbl_status.config(text="✖ PIN INCORRECTO. ACCESO DENEGADO.", fg="#e74c3c")
        entry_pin.delete(0, tk.END)

# --- Configuración de la Ventana (UI) ---
root = tk.Tk()
root.title("Terminal de Validación - Red Loica")
root.geometry("450x320")
root.configure(bg="#1e272e")
root.resizable(False, False)

# Elementos gráficos
lbl_titulo = tk.Label(root, text="NODO MAESTRO OFF-GRID", font=("Segoe UI", 16, "bold"), bg="#1e272e", fg="#d2dae2")
lbl_titulo.pack(pady=20)

lbl_instruccion = tk.Label(root, text="Ingrese PIN de seguridad (Dirigente):", font=("Segoe UI", 11), bg="#1e272e", fg="#808e9b")
lbl_instruccion.pack()

entry_pin = tk.Entry(root, show="*", font=("Courier", 24, "bold"), width=8, justify="center", bg="#2f3640", fg="#f5f6fa", insertbackground="white")
entry_pin.pack(pady=15)

btn_activar = tk.Button(root, text="VALIDAR Y TRANSMITIR", font=("Segoe UI", 12, "bold"), bg="#ff3f34", fg="white", activebackground="#ff5e57", activeforeground="white", command=validar_pin, width=25, height=2, bd=0, cursor="hand2")
btn_activar.pack(pady=5)

lbl_status = tk.Label(root, text="Sistema en modo de espera (Standby)", font=("Segoe UI", 9, "italic"), bg="#1e272e", fg="#485460")
lbl_status.pack(pady=15)

# Ejecutar aplicación
if __name__ == "__main__":
    root.mainloop()