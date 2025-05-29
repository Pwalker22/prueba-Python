import pandas as pd
from datetime import datetime

def export_to_excel(data):
    if not data:
        print("⚠️ No hay datos para exportar.")
        return

    # Convertir la lista de diccionarios en un DataFrame
    df = pd.DataFrame(data)

    # Generar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"seguidores_exportados_{timestamp}.xlsx"

    # Exportar a Excel
    df.to_excel(filename, index=False)
    print(f"✅ Datos exportados a {filename}")
