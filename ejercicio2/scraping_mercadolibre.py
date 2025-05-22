from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def buscar_productos(palabra):
    print(f"\n Resultados: '{palabra}'\n")

    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://listado.mercadolibre.com.co/{palabra}"
    driver.get(url)

    try:
       
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.ui-search-layout__item"))
        )

        for i in range(5):  
            try:
                
                productos = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ui-search-layout__item"))
                )

                producto = productos[i]

                
                try:
                    enlace_elemento = producto.find_element(By.CSS_SELECTOR, "a.poly-component__title")
                except:
                    enlace_elemento = producto.find_element(By.CSS_SELECTOR, "a.ui-search-item__group__element")

                titulo = enlace_elemento.text.strip()
                enlace = enlace_elemento.get_attribute("href")

                
                precio = producto.find_element(By.CSS_SELECTOR, "span.andes-money-amount__fraction").text.strip()

                
                try:
                    centavos = producto.find_element(By.CSS_SELECTOR, "span.andes-money-amount__cents").text.strip()
                    precio = f"{precio},{centavos}"
                except:
                    pass  

                print(f" Producto {i + 1}")
                print(f"Título: {titulo}")
                print(f" Precio: ${precio}")
                print(f" URL: {enlace}")
                print("-" * 50)

            except Exception as e:
                print(f" Error procesando producto {i + 1}: {e}")

    except Exception as e:
        print(f" Error al cargar los productos: {e}")

    driver.quit()


if __name__ == "__main__":
    palabra = input(" Ingresa el producto a buscar: ")
    buscar_productos(palabra)
