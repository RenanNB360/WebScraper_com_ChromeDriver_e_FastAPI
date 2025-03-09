import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service


def scraper_chromedrive(website):
    chrome_driver_path = '/usr/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    driver = None

    try:
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        print(f'Acessando o website: {website}')

        driver.get(website)
        time.sleep(10)

        html = driver.page_source
        print('Website acessado com sucesso.')
        return html

    except TimeoutException:
        print('Erro: Tempo de espera excedido ao tentar acessar o website.')
        return None

    except WebDriverException as e:
        print(f'Erro no WebDriver: {e}')
        return None

    except Exception as e:
        print(f'Erro inesperado ao acessar o website: {e}')
        return None

    finally:
        if driver:
            print('Fechando o navegador...')
            driver.quit()


def extract_text_chromedrive(html_content):
    try:
        if not html_content:
            raise ValueError('O conteúdo HTML está vazio ou é inválido.')

        soup = BeautifulSoup(html_content, 'html.parser')
        body_content = soup.body

        if body_content:
            return body_content.get_text()
        else:
            print('Erro: Nenhum conteúdo encontrado na tag <body>.')
            return None

    except Exception as e:
        print(f'Erro ao extrair texto do HTML: {e}')
        return None


def clean_body_content_chromedrive(body_content):
    try:
        if not body_content or not isinstance(body_content, str):
            return None

        soup = BeautifulSoup(body_content, 'html.parser')

        for script in soup(['script', 'style']):
            script.extract()

        cleaned_content = soup.get_text(separator='\n')
        cleaned_content = '\n'.join([line.strip() for line in cleaned_content.splitlines() if line.strip()])

        return cleaned_content if cleaned_content else None

    except Exception as e:
        print(f'Erro ao limpar o conteúdo do corpo: {e}')
        return None


def split_dom_content_chromedrive(dom_content, max_length=6000):
    try:
        if not dom_content:
            raise ValueError('O conteúdo DOM está vazio ou é inválido.')

        # Divide o conteúdo em partes menores
        return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]

    except Exception as e:
        print(f'Erro ao dividir o conteúdo DOM: {e}')
        return None
