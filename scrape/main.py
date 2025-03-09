from fastapi import FastAPI, HTTPException, status

from scrape.schema import URL, Message
from scrape.web_scrapers.webscraper_chromedriver import (
    clean_body_content_chromedrive,
    extract_text_chromedrive,
    scraper_chromedrive,
)

app = FastAPI()


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
async def index():
    return Message(
        message='Durante a extração de dados, você pode enfrentar riscos como violação de direitos autorais, '
        'invasão de privacidade e sobrecarga de servidores, além de cometer crimes como acesso não autorizado, '
        'espionagem industrial e discriminação.'
    )


@app.post('/scrape_chromedrive', status_code=status.HTTP_200_OK)
async def scraper_page_chromedrive(url: URL):
    try:
        result = scraper_chromedrive(url.url)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Falha ao acessar o website. Verifique a URL e tente novamente.'
            )

        body_content = extract_text_chromedrive(result)
        if body_content is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Falha ao extrair texto do HTML. O conteúdo pode estar vazio ou malformado.'
            )

        cleaned_content = clean_body_content_chromedrive(body_content)
        if cleaned_content is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Falha ao limpar o conteúdo do corpo. O conteúdo pode estar vazio ou malformado.',
            )

        return {'page_source': cleaned_content}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Erro inesperado durante o processamento: {str(e)}')
