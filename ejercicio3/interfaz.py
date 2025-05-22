import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

from base_datos import validar_usuario


def obtener_personajes_info():
    try:
        respuesta = requests.get("https://rickandmortyapi.com/api/character")
        datos = respuesta.json()
        personajes = []
        for p in datos["results"]:
            personajes.append({
                "nombre": p["name"],
                "imagen": p["image"],
                "especie": p["species"],
                "episodios": p["episode"]  
            })
        return personajes
    except Exception as e:
        print("Error al obtener personajes:", e)
        return []

def obtener_numero_episodio(url_episodio):
    if not url_episodio:
        return "Desconocido"
    return url_episodio.rstrip('/').split('/')[-1]


def login():
    usuario = entrada_usuario.get()
    clave = entrada_clave.get()
    print(f"Intento login: usuario={usuario}, clave={clave}")  # Debug

    if validar_usuario(usuario, clave):
        messagebox.showinfo("Bienvenido", "Login exitoso.")
        mostrar_personajes()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")


def mostrar_personajes():
    ventana_lista = tk.Toplevel()
    ventana_lista.title("Personajes de Rick and Morty")
    ventana_lista.geometry("600x700")

    contenedor = ttk.Frame(ventana_lista)
    contenedor.pack(fill="both", expand=True)

    canvas = tk.Canvas(contenedor)
    scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame.imagenes_tk = []

    def cargar_datos():
        personajes = obtener_personajes_info()
        if not personajes:
            
            ventana_lista.after(0, lambda: (
                messagebox.showerror("Error", "No se pudo conectar a la API."),
                ventana_lista.destroy()
            ))
            return
        
        for personaje in personajes:
            def crear_frame(p=personaje):
                frame_personaje = ttk.Frame(scrollable_frame, padding=10, relief="ridge")
                frame_personaje.pack(fill="x", pady=5, padx=5)

                ttk.Label(frame_personaje, text=f"Nombre: {p['nombre']}", font=("Arial", 14, "bold")).grid(row=0, column=1, sticky="w", padx=10)
                ttk.Label(frame_personaje, text=f"Tipo: {p['especie']}", font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=10)

                numero_ep = obtener_numero_episodio(p["episodios"][0]) if p["episodios"] else "Desconocido"
                ttk.Label(frame_personaje, text=f"Número de episodio: {numero_ep}", font=("Arial", 12)).grid(row=2, column=1, sticky="w", padx=10)

               
                def cargar_imagen():
                    try:
                        response = requests.get(p["imagen"])
                        img_data = response.content
                        img_pil = Image.open(BytesIO(img_data))
                        img_pil = img_pil.resize((80, 80), Image.LANCZOS)
                        img_tk = ImageTk.PhotoImage(img_pil)
                        scrollable_frame.imagenes_tk.append(img_tk)
                        def poner_imagen():
                            label_img = ttk.Label(frame_personaje, image=img_tk)
                            label_img.grid(row=0, column=0, rowspan=3, sticky="w")
                        ventana_lista.after(0, poner_imagen)
                    except Exception as e:
                        print("Error cargando imagen:", e)
                        def poner_texto():
                            label_img = ttk.Label(frame_personaje, text="[Sin imagen]")
                            label_img.grid(row=0, column=0, rowspan=3, sticky="w")
                        ventana_lista.after(0, poner_texto)
                
                threading.Thread(target=cargar_imagen).start()

            # Crear el frame en el hilo principal
            ventana_lista.after(0, crear_frame)

    threading.Thread(target=cargar_datos).start()


ventana = tk.Tk()
ventana.title("Login - Rick and Morty API")
ventana.geometry("320x300")
ventana.resizable(False, False)

frame_login = ttk.Frame(ventana, padding=20)
frame_login.pack(expand=True, fill="both")

ttk.Label(frame_login, text="Iniciar Sesión", font=("Arial", 18, "bold")).pack(pady=10)
ttk.Label(frame_login, text="Usuario:").pack(anchor="w")
entrada_usuario = ttk.Entry(frame_login, width=30)
entrada_usuario.pack(pady=5)
ttk.Label(frame_login, text="Contraseña:").pack(anchor="w")
entrada_clave = ttk.Entry(frame_login, show="*", width=30)
entrada_clave.pack(pady=5)
ttk.Button(frame_login, text="Iniciar sesión", command=login).pack(pady=15)

ventana.mainloop()
