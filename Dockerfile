FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . /app/

RUN apt update && apt install -y \
    wget curl unzip \
    libglib2.0-0 libnss3 libx11-xcb1 libxcomposite1 \
    libxcursor1 libxdamage1 libxi6 libxrandr2 \
    libgbm1 libgtk-3-0 libasound2 \
    chromium chromium-driver

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "scrape.main:app", "--host", "0.0.0.0", "--port", "8000"]