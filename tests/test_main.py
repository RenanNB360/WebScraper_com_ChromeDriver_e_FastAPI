from fastapi import status
from fastapi.testclient import TestClient

from scrape.main import app

client = TestClient(app)


def test_index():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK, 'O status code deve ser 200.'
    assert response.json() == {
        'message': 'Durante a extração de dados, você pode enfrentar riscos como violação de direitos autorais, '
        'invasão de privacidade e sobrecarga de servidores, além de cometer crimes como acesso não autorizado, '
        'espionagem industrial e discriminação.'
    }, 'A mensagem retornada deve corresponder ao esperado.'


def test_scrape_chromedrive_success(monkeypatch):
    def mock_scraper_chromedrive(url):
        return '<html><body>Test</body></html>'

    def mock_extract_text_chromedrive(html):
        return 'Test'

    def mock_clean_body_content_chromedrive(body_content):
        return 'Test'

    monkeypatch.setattr('scrape.main.scraper_chromedrive', mock_scraper_chromedrive)
    monkeypatch.setattr('scrape.main.extract_text_chromedrive', mock_extract_text_chromedrive)
    monkeypatch.setattr('scrape.main.clean_body_content_chromedrive', mock_clean_body_content_chromedrive)

    response = client.post('/scrape_chromedrive', json={'url': 'https://www.example.com'})
    assert response.status_code == status.HTTP_200_OK, 'O status code deve ser 200.'
    assert response.json() == {'page_source': 'Test'}, 'O conteúdo retornado deve corresponder ao esperado.'


def test_scrape_chromedrive_failed_scraping(monkeypatch):
    def mock_scraper_chromedrive(url):
        return None

    monkeypatch.setattr('scrape.web_scrapers.webscraper_chromedriver.scraper_chromedrive', mock_scraper_chromedrive)

    response = client.post('/scrape_chromedrive', json={'url': 'https://www.invalid.com'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, 'O status code deve ser 400.'
    assert response.json() == {'detail': 'Falha ao acessar o website. Verifique a URL e tente novamente.'}, (
        'A mensagem de erro deve corresponder ao esperado.'
    )


def test_scrape_chromedrive_failed_extraction(monkeypatch):
    def mock_scraper_chromedrive(url):
        return '<html><body>Test</body></html>'

    def mock_extract_text_chromedrive(html):
        return None

    monkeypatch.setattr('scrape.main.scraper_chromedrive', mock_scraper_chromedrive)
    monkeypatch.setattr('scrape.main.extract_text_chromedrive', mock_extract_text_chromedrive)

    response = client.post('/scrape_chromedrive', json={'url': 'https://www.example.com'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, 'O status code deve ser 400.'
    assert response.json() == {'detail': 'Falha ao extrair texto do HTML. O conteúdo pode estar vazio ou malformado.'}, (
        'A mensagem de erro deve corresponder ao esperado.'
    )


def test_scrape_chromedrive_failed_cleaning(monkeypatch):
    def mock_scraper_chromedrive(url):
        return '<html><body>Test</body></html>'

    def mock_extract_text_chromedrive(html):
        return 'Test'

    def mock_clean_body_content_chromedrive(body_content):
        return None

    monkeypatch.setattr('scrape.main.scraper_chromedrive', mock_scraper_chromedrive)
    monkeypatch.setattr('scrape.main.extract_text_chromedrive', mock_extract_text_chromedrive)
    monkeypatch.setattr('scrape.main.clean_body_content_chromedrive', mock_clean_body_content_chromedrive)

    response = client.post('/scrape_chromedrive', json={'url': 'https://www.example.com'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, 'O status code deve ser 400.'
    assert response.json() == {'detail': 'Falha ao limpar o conteúdo do corpo. O conteúdo pode estar vazio ou malformado.'}, (
        'A mensagem de erro deve corresponder ao esperado.'
    )


def test_scrape_chromedrive_unexpected_error(monkeypatch):
    def mock_scraper_chromedrive(url):
        raise Exception('Erro inesperado')

    monkeypatch.setattr('scrape.main.scraper_chromedrive', mock_scraper_chromedrive)

    response = client.post('/scrape_chromedrive', json={'url': 'https://www.example.com'})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR, 'O status code deve ser 500.'
    assert response.json() == {'detail': 'Erro inesperado durante o processamento: Erro inesperado'}, (
        'A mensagem de erro deve corresponder ao esperado.'
    )
