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
        # Inicializar el inventario con los 4 productos
        self.productos = {
            "botella_agua": 5,
            "papas_fritas": 4,
            "lata_refresco": 3,
            "barra_chocolate": 3
        }

    def actualizar_inventario(self, producto):
        if self.productos[producto] > 0:
            self.productos[producto] -= 1
            print(f"Producto {producto} retirado. Inventario actualizado: {self.productos[producto]} restantes")
            self.verificar_inventario_bajo(producto)
        else:
            print(f"Producto {producto} agotado")

    def mostrar_inventario(self):
        print("Inventario actual:")
        for producto, cantidad in self.productos.items():
            print(f"{producto}: {cantidad} unidades")

    def verificar_inventario_bajo(self, producto):
        if self.productos[producto] < 2:
            print(f"ALERTA: {producto} está a punto de agotarse")
            messagebox.showwarning("Inventario Bajo", f"ALERTA: {producto} está a punto de agotarse")

# Función para detección de personas y productos
def detectar(frame):
    results = model(frame)
    productos_detectados = []

    # Iterar sobre cada resultado en results
    for result in results:
        boxes = result.boxes  # Obtener las cajas detectadas
        for box in boxes:
            # Coordenadas del cuadro delimitador
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            clase = int(box.cls[0])  # Obtener la clase de la detección

            # Dibujar el cuadro delimitador
            if clase == 0:  # Clase 0 corresponde a 'persona' en el modelo YOLOv8 por defecto
                label = "Persona"
                color = (0, 255, 0)  # Verde para personas
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print("Persona detectada")
            elif clase == 39:  # Clase para botellas, ajusta según el dataset
                label = "Botella de Agua"
                color = (255, 0, 0)  # Azul para botellas
                productos_detectados.append("botella_agua")
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print("Botella de agua detectada")
            elif clase == 41:  # Clase para bolsas de papas fritas
                label = "Papas Fritas"
                color = (0, 0, 255)  # Rojo para papas fritas
                productos_detectados.append("papas_fritas")
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print("Bolsa de papas fritas detectada")
            elif clase == 72:  # Clase para latas de refresco
                label = "Lata de Refresco"
                color = (255, 255, 0)  # Amarillo para latas
                productos_detectados.append("lata_refresco")
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print("Lata de refresco detectada")
            elif clase == 43:  # Clase para barras de chocolate
                label = "Barra de Chocolate"
                color = (0, 255, 255)  # Cian para barras de chocolate
                productos_detectados.append("barra_chocolate")
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                print("Barra de chocolate detectada")

    return productos_detectados

# Crear la interfaz gráfica con Tkinter
def iniciar_interfaz_grafica(inventario):
    ventana = tk.Tk()
    ventana.title("Inventario en Tiempo Real")

    # Etiquetas para mostrar los productos
    etiqueta_agua = tk.Label(ventana, text=f"Botellas de agua: {inventario.productos['botella_agua']}")
    etiqueta_agua.pack()

    etiqueta_papas = tk.Label(ventana, text=f"Bolsas de papas fritas: {inventario.productos['papas_fritas']}")
    etiqueta_papas.pack()

    etiqueta_refresco = tk.Label(ventana, text=f"Latas de refresco: {inventario.productos['lata_refresco']}")
    etiqueta_refresco.pack()

    etiqueta_chocolate = tk.Label(ventana, text=f"Barras de chocolate: {inventario.productos['barra_chocolate']}")
    etiqueta_chocolate.pack()

    # Función para actualizar la interfaz gráfica cada vez que cambie el inventario
    def actualizar_inventario_grafico():
        etiqueta_agua.config(text=f"Botellas de agua: {inventario.productos['botella_agua']}")
        etiqueta_papas.config(text=f"Bolsas de papas fritas: {inventario.productos['papas_fritas']}")
        etiqueta_refresco.config(text=f"Latas de refresco: {inventario.productos['lata_refresco']}")
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
        productos_detectados = detectar(frame)

        # Actualizar el inventario si un producto es retirado
        for producto in productos_detectados:
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