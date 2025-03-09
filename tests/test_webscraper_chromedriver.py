from selenium.common.exceptions import TimeoutException

from scrape.web_scrapers.webscraper_chromedriver import (
    clean_body_content_chromedrive,
    extract_text_chromedrive,
    scraper_chromedrive,
    split_dom_content_chromedrive,
)

len_result = 2
len_part = 5000


def test_scraper_chromedrive_success():
    url = 'https://www.example.com'  # URL de exemplo
    result = scraper_chromedrive(url)
    assert result is not None, 'O scraping falhou. O resultado não deve ser None.'
    assert '<html' in result.lower(), 'O resultado deve conter um HTML válido.'


def test_scraper_chromedrive_invalid_url():
    url = 'https://www.urlinvalida.com'  # URL inválida
    result = scraper_chromedrive(url)
    assert result is None, 'O scraping de uma URL inválida deve retornar None.'


def test_scraper_chromedrive_empty_url():
    url = ''  # URL vazia
    result = scraper_chromedrive(url)
    assert result is None, 'O scraping de uma URL vazia deve retornar None.'


def test_extract_text_chromedrive_success():
    html_content = '<html><body><p>Hello, World!</p></body></html>'
    result = extract_text_chromedrive(html_content)
    assert result is not None, 'A extração de texto falhou. O resultado não deve ser None.'
    assert 'Hello, World!' in result, "O texto extraído deve conter 'Hello, World!'."


def test_extract_text_chromedrive_empty_html():
    html_content = ''
    result = extract_text_chromedrive(html_content)
    assert result is None, 'A extração de texto de um HTML vazio deve retornar None.'


def test_extract_text_chromedrive_invalid_html():
    html_content = '<invalid>'
    result = extract_text_chromedrive(html_content)
    assert result is None, 'A extração de texto de um HTML inválido deve retornar None.'


def test_clean_body_content_chromedrive_success():
    body_content = "<body><p>Hello, World!</p><script>alert('test');</script></body>"
    result = clean_body_content_chromedrive(body_content)
    assert result is not None, 'A limpeza do conteúdo falhou. O resultado não deve ser None.'
    assert 'Hello, World!' in result, "O conteúdo limpo deve conter 'Hello, World!'."
    assert "alert('test');" not in result, 'O conteúdo limpo não deve conter scripts.'


def test_clean_body_content_chromedrive_empty_content():
    body_content = ''
    result = clean_body_content_chromedrive(body_content)
    assert result is None, 'A limpeza de conteúdo vazio deve retornar None.'


def test_clean_body_content_chromedrive_invalid_content():
    body_content = '<invalid>'
    result = clean_body_content_chromedrive(body_content)
    assert result is None, 'A limpeza de conteúdo inválido deve retornar None.'


def test_split_dom_content_chromedrive_success():
    dom_content = 'a' * 10000
    result = split_dom_content_chromedrive(dom_content, max_length=5000)
    assert result is not None, 'A divisão do conteúdo falhou. O resultado não deve ser None.'
    assert len(result) == len_result, 'O conteúdo deve ser dividido em 2 partes.'
    assert all(len(part) <= len_part for part in result), 'Cada parte deve ter no máximo 5000 caracteres.'


def test_split_dom_content_chromedrive_empty_content():
    dom_content = ''
    result = split_dom_content_chromedrive(dom_content)
    assert result is None, 'A divisão de conteúdo vazio deve retornar None.'


def test_split_dom_content_chromedrive_invalid_max_length():
    dom_content = 'a' * 100
    result = split_dom_content_chromedrive(dom_content, max_length=0)
    assert result is None, 'A divisão com max_length inválido deve retornar None.'


def test_scraper_chromedrive_timeout_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise TimeoutException('Tempo de espera excedido')

    monkeypatch.setattr('selenium.webdriver.Chrome.get', mock_get)

    result = scraper_chromedrive('https://www.example.com')
    assert result is None, 'A função deve retornar None em caso de TimeoutException.'


def test_scraper_chromedrive_generic_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise Exception('Erro inesperado')

    monkeypatch.setattr('selenium.webdriver.Chrome.get', mock_get)

    result = scraper_chromedrive('https://www.example.com')
    assert result is None, 'A função deve retornar None em caso de exceção genérica.'


def test_clean_body_content_chromedrive_exception(monkeypatch):
    def mock_beautifulsoup(*args, **kwargs):
        raise Exception('Erro ao processar HTML')

    monkeypatch.setattr('scrape.web_scrapers.webscraper_chromedriver.BeautifulSoup', mock_beautifulsoup)

    result = clean_body_content_chromedrive('<html><body>Test</body></html>')
    assert result is None, 'A função deve retornar None em caso de exceção.'
