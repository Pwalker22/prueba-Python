import time
from scraper import scrape_followers_data, create_driver
from excel_exporter import export_to_excel

# Constantes
CUENTAS = ["elcorteingles", "mercadona", "carrefoures"]
NUM_SEGUIDORES = 10  # Cambia este valor si deseas más seguidores por cuenta

# ✅ Crear el WebDriver con perfil temporal desde scraper.py
driver = create_driver()

# Abrir Instagram
driver.get("https://www.instagram.com/")
time.sleep(5)  # Esperar a que cargue la página

# Verificar si estamos logueados
if "login" in driver.current_url:
    print("⚠️ No se detectó sesión iniciada. Por favor, inicia sesión manualmente.")
    input("🔐 Presiona ENTER cuando hayas iniciado sesión...")
else:
    print("✅ Sesión iniciada correctamente.")

# Extraer datos de los seguidores
datos = []
for cuenta in CUENTAS:
    print(f"🔍 Extrayendo seguidores de: {cuenta}")
    datos += scrape_followers_data(driver, cuenta, NUM_SEGUIDORES)

# Exportar datos a archivo Excel
export_to_excel(datos)

# Cerrar navegador
driver.quit()
print("📁 Extracción completada y exportada a Excel.")
