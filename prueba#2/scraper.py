from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import tempfile
import time
from utils import extract_emails, extract_phones  # Asegúrate que estas funciones estén definidas

def create_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    # options.add_argument("--remote-debugging-port=9222")  # <-- Línea removida para evitar error de puerto
    # options.add_argument("--headless=new")  # Descomenta si no quieres abrir navegador visible

    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    print("✅ Navegador abierto")
    return driver


def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")

    # Espera y llena campos
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)

    try:
        # Espera que cambie la url y aparezca el icono de perfil en la barra superior
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt*='profile picture']"))
        )
        print("✅ Sesión iniciada correctamente.")
        return True
    except TimeoutException:
        print("❌ No se pudo iniciar sesión: probable captcha, bloqueo o error en credenciales.")
        return False
def scrape_followers_data(driver, target_account, max_followers=50):
    print(f"➡️ Abriendo perfil de {target_account}")
    driver.get(f"https://www.instagram.com/{target_account}/")

    try:
        followers_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
        )
        followers_button.click()
        print("✅ Botón de seguidores encontrado y clickeado")
    except TimeoutException:
        print(f"❌ No se pudo encontrar el botón de seguidores en la cuenta: {target_account}")
        return []

    try:
        followers_popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//ul"))
        )
        print("✅ Ventana emergente de seguidores abierta")
    except TimeoutException:
        print("❌ No se pudo abrir la ventana emergente de seguidores.")
        return []

    scrolls = max_followers // 10 + 2
    for i in range(scrolls):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_popup)
        time.sleep(2)
        print(f"➡️ Scroll #{i + 1} en lista de seguidores")

    followers = followers_popup.find_elements(By.XPATH, ".//li//a")[:max_followers]
    urls = [f.get_attribute("href") for f in followers if f.get_attribute("href")]

    info = []
    for idx, url in enumerate(urls, 1):
        print(f"➡️ Procesando seguidor #{idx}: {url}")
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "section"))
            )
        except TimeoutException:
            print(f"⚠️ No se pudo cargar el perfil: {url}")
            continue

        try:
            name = driver.find_element(By.XPATH, "//section//h1").text
        except NoSuchElementException:
            name = ""

        try:
            bio = driver.find_element(By.XPATH, "//div[contains(@class,'-vDIg')]/span").text
        except NoSuchElementException:
            bio = ""

        date = "Fecha desconocida"
        try:
            posts = driver.find_elements(By.XPATH, "//article//a")
            if posts:
                first_post_url = posts[0].get_attribute("href")
                if first_post_url:
                    driver.get(first_post_url)
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.TAG_NAME, "time"))
                    )
                    date = driver.find_element(By.TAG_NAME, "time").get_attribute("datetime")
        except:
            pass

        info.append({
            "nombre": name,
            "telefono": extract_phones(bio),
            "email": extract_emails(bio),
            "fecha_creacion": date,
            "perfil": url
        })

    return info

# Ejemplo de uso:
# driver = login_instagram("tu_usuario", "tu_contraseña")
# if driver:
#     seguidores = scrape_followers_data(driver, "nombre_de_la_cuenta_objetivo", 30)
#     driver.quit()
#     print(seguidores)
