
# **Documentación del Sistema de Detección de Personas y Monitoreo de Inventario con YOLOv8**

## **1. Introducción**

Este proyecto implementa un sistema de detección automática de personas y monitoreo de productos en una tienda virtual utilizando **YOLOv8** para la detección de objetos y personas. El sistema es capaz de:

- Detectar personas en tiempo real utilizando la cámara del dispositivo.
- Detectar y rastrear diferentes productos (botellas de agua, papas fritas, latas de gaseosa, barras de chocolate).
- Monitorear y actualizar dinámicamente el inventario conforme los productos se van detectando.
- Mostrar una interfaz gráfica en tiempo real para reflejar el estado del inventario.

## **2. Requisitos Técnicos**

Antes de ejecutar el sistema, se deben cumplir los siguientes requisitos:

- **Python 3.x**
- Librerías necesarias:
  - `ultralytics`: Implementación de **YOLOv8** para la detección de objetos y personas.
  - `opencv-python`: Para la captura de video y procesamiento de imágenes en tiempo real.
  - `tkinter`: Para crear la interfaz gráfica del inventario.
  
Instalar las dependencias necesarias:

```bash
pip install ultralytics opencv-python tkintertable
```

## **3. Estructura del Sistema**

### 3.1. **YOLOv8: Detección de Objetos**

La detección de personas y productos está basada en el modelo YOLOv8. El modelo preentrenado se utiliza para detectar objetos dentro de los frames capturados en tiempo real por la cámara. Las clases específicas de productos y personas ya están definidas en el modelo y mapeadas a categorías específicas:

- Clase 0: Persona
- Clase 39: Botellas de agua
- Clase 41: Bolsas de papas fritas
- Clase 72: Latas de gaseosa
- Clase 43: Barras de chocolate

#### **Decisiones:**

- **Uso de YOLOv8**: Elegimos YOLOv8 por su capacidad de realizar detecciones rápidas y precisas en tiempo real. Además, el modelo ya tiene preentrenadas muchas de las clases de objetos que queríamos detectar, como personas y ciertos productos.

### 3.2. **Inventario Dinámico**

El inventario no está predefinido. Se actualiza de manera dinámica cuando un producto es detectado por primera vez. Esto permite que el sistema inicialice automáticamente productos conforme son vistos por la cámara. Cada vez que un producto es detectado, el inventario incrementa su contador para ese producto.

#### **Decisiones:**

- **Inicialización dinámica del inventario**: Para evitar tener un inventario predefinido, decidimos inicializar los productos solo cuando aparecen por primera vez en el marco. Esto asegura que el inventario refleje fielmente los productos reales que se ven a través de la cámara.
- **Actualización de inventario**: Cada vez que un producto es detectado, su contador se incrementa para llevar un control preciso del número de veces que ha aparecido en la cámara.

### 3.3. **Detección de Personas**

El sistema detecta la presencia de personas y emite un mensaje tanto en la consola como en la interfaz gráfica. No se lleva un inventario de personas, pero la detección sirve para saber si hay actividad en la tienda.

#### **Decisiones:**

- **Presencia de personas**: Decidimos incluir la detección de personas para simular la llegada de clientes a la tienda. Esto agrega un nivel de interacción que refleja una tienda real donde los productos son tomados por personas.

### 3.4. **Interfaz Gráfica con Tkinter**

Se ha utilizado **Tkinter** para crear una interfaz gráfica que muestre en tiempo real el estado del inventario. Conforme los productos se van detectando, el inventario se actualiza dinámicamente en la ventana.

#### **Elementos de la Interfaz:**

- **Etiquetas de productos**: Se crean etiquetas para cada producto (botellas de agua, papas fritas, latas de gaseosa y barras de chocolate). Si un producto no ha sido detectado aún, la interfaz muestra un mensaje de "Esperando detección".
- **Actualización automática**: La interfaz se actualiza cada segundo para reflejar los cambios en el inventario, asegurando que el usuario vea el estado en tiempo real.

#### **Decisiones:**

- **Uso de Tkinter**: Tkinter es una biblioteca ligera que viene preinstalada con Python. Es fácil de integrar y permite crear una interfaz gráfica sencilla pero efectiva para mostrar el estado del inventario.
- **Actualización en tiempo real**: Se optó por usar el método `after()` de Tkinter para refrescar periódicamente el estado del inventario, logrando así una interfaz dinámica que se actualiza sin congelar la ejecución del programa principal.

### 3.5. **Integración de Hilos (Threading)**

Dado que tanto el proceso de captura de video como la interfaz gráfica deben ejecutarse simultáneamente, se utilizó **Threading** para ejecutar la interfaz en un hilo separado. Esto permite que ambos procesos (captura de video y la interfaz) funcionen en paralelo sin bloquearse mutuamente.

#### **Decisiones:**

- **Uso de hilos**: Para evitar que la interfaz gráfica bloquee la captura de video, se ejecuta en un hilo separado. Esto garantiza que tanto la interfaz como la detección de objetos funcionen de manera simultánea y fluida.

## **4. Flujo del Sistema**

1. **Inicialización del Modelo y la Cámara**:
   - Se carga el modelo YOLOv8 preentrenado y se inicializa la captura de video usando la cámara.

2. **Ejecución de la Interfaz Gráfica**:
   - La interfaz gráfica se lanza en un hilo separado para que el usuario pueda ver el estado del inventario mientras el sistema está operando.

3. **Detección en Tiempo Real**:
   - Cada frame capturado por la cámara se procesa a través del modelo YOLOv8 para identificar personas y productos.
   - Los productos detectados se inicializan en el inventario la primera vez que aparecen y, posteriormente, su contador se actualiza con cada detección.

4. **Actualización de la Interfaz**:
   - La interfaz gráfica se actualiza periódicamente para reflejar el estado actual del inventario en tiempo real.

5. **Finalización**:
   - El usuario puede salir del programa presionando la tecla 'q', lo que detiene la captura de video y cierra la ventana de la interfaz gráfica.

## **5. Decisiones Clave**

1. **Detección Dinámica de Productos**: Se decidió no predefinir el inventario, sino inicializarlo dinámicamente conforme los productos son detectados. Esto refleja un comportamiento más realista de una tienda, donde los productos solo se cuentan cuando son vistos.

2. **Uso de YOLOv8 Preentrenado**: Elegimos un modelo preentrenado para evitar el proceso costoso de entrenamiento desde cero. Las clases de objetos utilizadas ya estaban presentes en el modelo, lo que simplificó su uso.

3. **Interfaz Gráfica Separada**: El uso de Tkinter en un hilo separado asegura que el monitoreo en tiempo real y la interfaz funcionen sin interrupciones.

## **6. Posibles Mejoras**

1. **Detección de Productos Agotados**: Se podría mejorar el sistema para marcar productos como "agotados" una vez que se detecten una cantidad determinada de veces.

2. **Sistema de Notificaciones Mejorado**: Integrar notificaciones más avanzadas o una función de alerta sonora cuando se detecte que un producto está por agotarse.

3. **Almacenamiento de Datos**: Se podría agregar la funcionalidad de almacenar el historial de detección de productos en una base de datos o archivo, para llevar un control histórico del inventario.

## **7. Conclusión**

Este sistema combina la potencia de la detección de objetos en tiempo real con una interfaz gráfica para monitorear el inventario de una tienda virtual. Las decisiones técnicas, como el uso de YOLOv8, inventario dinámico y la separación en hilos, garantizan que el sistema funcione de manera eficiente y fluida, proporcionando una solución simple pero efectiva para el monitoreo de productos y la detección de personas.
