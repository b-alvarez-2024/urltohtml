import os
import tkinter as tk
from tkinter import filedialog, messagebox

def convertir_url_a_html(ruta_archivo_url, ruta_archivo_html):
    """Convierte un archivo .url a un archivo .html con redirección (formato optimizado)."""
    print(f"Intentando convertir: {ruta_archivo_url} a {ruta_archivo_html}")
    try:
        with open(ruta_archivo_url, 'r', encoding='utf-8') as archivo_url:
            url = None
            for linea in archivo_url:
                linea_limpia = linea.strip()
                if linea_limpia.startswith("URL="):
                    url = linea_limpia.split("=")[1].strip()
                    break
            if url:
                html_content = f"""<meta
http-equiv="refresh"
content="0; url={url}"
 />"""
                with open(ruta_archivo_html, 'w', encoding='utf-8') as archivo_html:
                    archivo_html.write(html_content)
                print(f"Éxito al convertir: {ruta_archivo_url} -> {ruta_archivo_html}")
                return True
            else:
                print(f"Error: No se encontró URL en: {ruta_archivo_url}")
                messagebox.showerror("Error", f"No se encontró la URL en: {ruta_archivo_url}")
                return False
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {ruta_archivo_url}")
        messagebox.showerror("Error", f"Archivo no encontrado: {ruta_archivo_url}")
        return False
    except Exception as e:
        mensaje_error_interno = f"Error inesperado al procesar {ruta_archivo_url}: {e}"
        print(mensaje_error_interno)
        messagebox.showerror("Error", mensaje_error_interno)
        return False

def seleccionar_carpeta_entrada():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta con archivos .url")
    carpeta_entrada_entry.delete(0, tk.END)
    carpeta_entrada_entry.insert(0, carpeta)
    print(f"Carpeta de entrada seleccionada: {carpeta}")

def seleccionar_carpeta_salida():
    carpeta = filedialog.askdirectory(title="Seleccionar carpeta de salida para archivos .html")
    carpeta_salida_entry.delete(0, tk.END)
    carpeta_salida_entry.insert(0, carpeta)
    print(f"Carpeta de salida seleccionada: {carpeta}")

def pegar_carpeta_entrada():
    try:
        carpeta = ventana.clipboard_get()
        carpeta_entrada_entry.delete(0, tk.END)
        carpeta_entrada_entry.insert(0, carpeta)
        print(f"Carpeta de entrada pegada: {carpeta}")
    except tk.TclError:
        messagebox.showerror("Error", "No hay nada en el portapapeles.")

def pegar_carpeta_salida():
    try:
        carpeta = ventana.clipboard_get()
        carpeta_salida_entry.delete(0, tk.END)
        carpeta_salida_entry.delete(0, tk.END)
        carpeta_salida_entry.insert(0, carpeta)
        print(f"Carpeta de salida pegada: {carpeta}")
    except tk.TclError:
        messagebox.showerror("Error", "No hay nada en el portapapeles.")

def cerrar_ventana():
    ventana.destroy()

def iniciar_conversion():
    carpeta_entrada = carpeta_entrada_entry.get().strip()
    carpeta_salida = carpeta_salida_entry.get().strip()
    eliminar_urls = eliminar_var.get()

    print(f"Iniciando conversión desde: '{carpeta_entrada}' a '{carpeta_salida}', Eliminar URLs: {eliminar_urls}")

    if not carpeta_entrada or not carpeta_salida:
        mensaje_error_seleccion = "Por favor, selecciona las carpetas de entrada y salida."
        print(f"Error: {mensaje_error_seleccion}")
        messagebox.showerror("Error", mensaje_error_seleccion)
        return

    archivos_convertidos = 0
    archivos_no_convertidos = 0
    try:
        for nombre_archivo in os.listdir(carpeta_entrada):
            if nombre_archivo.lower().endswith('.url'):
                ruta_url_completa = os.path.join(carpeta_entrada, nombre_archivo)
                nombre_base = os.path.splitext(nombre_archivo)[0]
                ruta_html_completa = os.path.join(carpeta_salida, f'{nombre_base}.html')
                if convertir_url_a_html(ruta_url_completa, ruta_html_completa):
                    archivos_convertidos += 1
                    if eliminar_urls:
                        try:
                            os.remove(ruta_url_completa)
                            print(f"Archivo .url eliminado: {ruta_url_completa}")
                        except Exception as e:
                            print(f"Error al eliminar {ruta_url_completa}: {e}")
                            messagebox.showerror("Error al Eliminar", f"No se pudo eliminar {ruta_url_completa}: {e}")
                else:
                    archivos_no_convertidos += 1
    except Exception as e:
        mensaje_error_global = f"Error inesperado durante la conversión por lote: {e}"
        print(mensaje_error_global)
        messagebox.showerror("Error", mensaje_error_global)
        return

    mensaje_final = f"Se convirtieron {archivos_convertidos} archivos .url a .html (formato optimizado).\n"
    if archivos_no_convertidos > 0:
        mensaje_final += f"No se pudieron convertir {archivos_no_convertidos} archivos. Verifica la terminal para más detalles."
    messagebox.showinfo("Conversión Completa", mensaje_final)
    print("Proceso de conversión completado.")

# --- INTERFAZ GRÁFICA CON TKINTER ---
ventana = tk.Tk()
ventana.title("Convertir .url a .html por Lote (Optimizado)")

# Etiqueta y campo de entrada para la carpeta de entrada
tk.Label(ventana, text="Carpeta de entrada (.url):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
boton_seleccionar_entrada = tk.Button(ventana, text="Seleccionar", command=seleccionar_carpeta_entrada)
boton_seleccionar_entrada.grid(row=0, column=1, padx=(0, 2), pady=5, sticky="ew")
boton_pegar_entrada = tk.Button(ventana, text="Pegar ruta", command=pegar_carpeta_entrada, width=10)  # Texto cambiado y ancho ajustado
boton_pegar_entrada.grid(row=0, column=2, padx=(0, 2), pady=5, sticky="ew")
carpeta_entrada_entry = tk.Entry(ventana, width=40)
carpeta_entrada_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

# Etiqueta y campo de entrada para la carpeta de salida
tk.Label(ventana, text="Carpeta de salida (.html):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
boton_seleccionar_salida = tk.Button(ventana, text="Seleccionar", command=seleccionar_carpeta_salida)
boton_seleccionar_salida.grid(row=1, column=1, padx=(0, 2), pady=5, sticky="ew")
boton_pegar_salida = tk.Button(ventana, text="Pegar ruta", command=pegar_carpeta_salida, width=10)  # Texto cambiado y ancho ajustado
boton_pegar_salida.grid(row=1, column=2, padx=(0, 2), pady=5, sticky="ew")
carpeta_salida_entry = tk.Entry(ventana, width=40)
carpeta_salida_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

# Checkbox para eliminar archivos .url
eliminar_var = tk.BooleanVar()
checkbox_eliminar = tk.Checkbutton(ventana, text="Eliminar .urls después de la conversión", variable=eliminar_var)
checkbox_eliminar.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")

# Botón para iniciar la conversión y botón para cerrar
boton_convertir = tk.Button(ventana, text="Iniciar Conversión", command=iniciar_conversion)
boton_convertir.grid(row=2, column=2, padx=(0, 5), pady=10, sticky="ew")
boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_ventana, width=7)  # Ancho ajustado ligeramente
boton_cerrar.grid(row=2, column=3, padx=(0, 5), pady=10, sticky="ew")

ventana.grid_columnconfigure(3, weight=1)
ventana.grid_columnconfigure(1, weight=0)
ventana.grid_columnconfigure(2, weight=0)

ventana.mainloop()