import cv2
from ultralytics import YOLO
import time
import tkinter as tk
from tkinter import messagebox
import threading

# Cargar el modelo preentrenado de YOLOv8
model = YOLO('yolov8s.pt')

# Inicializar el inventario
class Inventario:
    def __init__(self):
        # Inicializar el inventario vacío (productos se agregarán conforme se detecten)
        self.productos = {}

    def inicializar_producto(self, producto):
        if producto not in self.productos:
            self.productos[producto] = 0
            print(f"Producto {producto} inicializado en el inventario.")

    def actualizar_inventario(self, producto):
        # Aumentar el conteo del producto cuando es detectado
        if producto in self.productos:
            self.productos[producto] += 1
            print(f"Producto {producto} detectado. Inventario actualizado: {self.productos[producto]} detectados")
            self.verificar_inventario_bajo(producto)

    def mostrar_inventario(self):
        print("Inventario actual:")
        for producto, cantidad in self.productos.items():
            print(f"{producto}: {cantidad} detectados")

    def verificar_inventario_bajo(self, producto):
        if self.productos[producto] < 2:
            print(f"ALERTA: {producto} está a punto de agotarse")
            messagebox.showwarning("Inventario Bajo", f"ALERTA: {producto} está a punto de agotarse")

# Función para detección de personas y productos
def detectar(frame):
    results = model(frame)
    productos_detectados = []
    persona_detectada = False
    for result in results.xyxy[0]:
        clase = int(result[5])
        if clase == 0:  # Clase 0 corresponde a 'persona' en el modelo YOLOv8 por defecto
            persona_detectada = True
            print("Persona detectada")
        elif clase == 39:  # Clase para botellas, ajusta según el dataset
            print("Botella de agua detectada")
            productos_detectados.append("botella_agua")
        elif clase == 41:  # Clase para bolsas de papas fritas
            print("Bolsa de papas fritas detectada")
            productos_detectados.append("papas_fritas")
        elif clase == 72:  # Clase para latas de gaseosa
            print("Lata de gaseosa detectada")
            productos_detectados.append("lata_gaseosa")
        elif clase == 43:  # Clase para barras de chocolate
            print("Barra de chocolate detectada")
            productos_detectados.append("barra_chocolate")
    return persona_detectada, productos_detectados

# Crear la interfaz gráfica con Tkinter
def iniciar_interfaz_grafica(inventario):
    ventana = tk.Tk()
    ventana.title("Inventario en Tiempo Real")

    # Etiquetas para mostrar los productos
    etiqueta_agua = tk.Label(ventana, text="Esperando detección de botella de agua...")
    etiqueta_agua.pack()

    etiqueta_papas = tk.Label(ventana, text="Esperando detección de papas fritas...")
    etiqueta_papas.pack()

    etiqueta_gaseosa = tk.Label(ventana, text="Esperando detección de latas de gaseosa...")
    etiqueta_gaseosa.pack()

    etiqueta_chocolate = tk.Label(ventana, text="Esperando detección de barras de chocolate...")
    etiqueta_chocolate.pack()

    etiqueta_persona = tk.Label(ventana, text="Esperando detección de persona...")
    etiqueta_persona.pack()

    # Función para actualizar la interfaz gráfica cada vez que cambie el inventario
    def actualizar_inventario_grafico():
        if "botella_agua" in inventario.productos:
            etiqueta_agua.config(text=f"Botellas de agua: {inventario.productos['botella_agua']}")
        if "papas_fritas" in inventario.productos:
            etiqueta_papas.config(text=f"Bolsas de papas fritas: {inventario.productos['papas_fritas']}")
        if "lata_gaseosa" in inventario.productos:
            etiqueta_gaseosa.config(text=f"Latas de gaseosa: {inventario.productos['lata_gaseosa']}")
        if "barra_chocolate" in inventario.productos:
            etiqueta_chocolate.config(text=f"Barras de chocolate: {inventario.productos['barra_chocolate']}")

        ventana.after(1000, actualizar_inventario_grafico)

    # Iniciar la actualización periódica del inventario gráfico
    actualizar_inventario_grafico()

    ventana.mainloop()

# Inicializar el inventario
inventario = Inventario()

# Iniciar la interfaz gráfica en un hilo separado

interfaz_thread = threading.Thread(target=iniciar_interfaz_grafica, args=(inventario,))
interfaz_thread.start()

# Captura de video en tiempo real
cap = cv2.VideoCapture(0)

# Monitoreo de inventario en tiempo real
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detectar personas y productos
        persona_detectada, productos_detectados = detectar(frame)

        # Mostrar si se detecta una persona
        if persona_detectada:
            print("Persona detectada en la tienda.")

        # Inicializar y actualizar el inventario dinámicamente
        for producto in productos_detectados:
            inventario.inicializar_producto(producto)
            inventario.actualizar_inventario(producto)

        # Mostrar el frame con detecciones
        cv2.imshow("Tienda Automática", frame)

        # Presionar 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Pausa breve para reducir el uso de recursos
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Proceso detenido manualmente.")

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
