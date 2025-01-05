from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

app = Flask(__name__)

# Função para buscar os produtos
def search_product(product_name):

    # Configuração para rodar o Chrome sem interface (opcional)
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Rodar sem interface gráfica
    chrome_options.add_argument('--disable-gpu')  # Desabilitar o uso da GPU (necessário em alguns ambientes)
    chrome_options.add_argument('--no-sandbox')  # Necessário em ambientes de container como o Render
    chrome_options.add_argument('--disable-dev-shm-usage')  # Necessário em alguns ambientes com Docker
    chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/chrome"  # Caminho do Chrome no Render
    
    # Instalar e configurar o chromedriver automaticamente
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Ir para a página inicial
    website = "https://www.klikindomaret.com/"
    driver.get(website)

    # Esperar até o campo de pesquisa estar visível e interagir com ele
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='searchids']"))
    )
    search_box.send_keys(product_name)
    search_box.send_keys(Keys.RETURN)

    # Esperar até que os resultados sejam carregados (aguarda a presença dos produtos)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='wrp-content']//div[@class='title']"))
    )

    # Encontrar os produtos, preços e imagens
    products = driver.find_elements(By.XPATH, "//div[@class='wrp-content']//div[@class='title']")
    prices = driver.find_elements(By.XPATH, "//span[@class='normal price-value']")
    images = driver.find_elements(By.XPATH, "//div[@class='wrp-media']//img[@class='lazy loaded']")

    # Limitar aos 3 primeiros
    results = []
    for i in range(min(4, len(products))):
        product_image = images[i].get_attribute('data-src') or images[i].get_attribute('src')
        results.append({
            "name": products[i].text,
            "price": prices[i].text,
            "image": product_image
        })

    # Fechar o navegador
    driver.quit()

    return results

# Página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        results = search_product(product_name)
        return render_template('index.html', results=results, product_name=product_name)
    return render_template('index.html', results=[], product_name='')

# Configuração para rodar o app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
