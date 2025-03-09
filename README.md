# Web Scraper

Este projeto é um Web Scraper que coleta dados da web e os processa de forma automatizada. Ele utiliza Python, Docker e GitHub Actions para automação.

## 📌 Funcionalidades
- Extração de dados de sites
- Execução em ambiente Dockerizado
- Testes automatizados com pytest
- CI/CD com GitHub Actions

## 🚀 Como rodar o projeto

### 1️⃣ Clonar o repositório
```sh
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2️⃣ Construir e rodar com Docker Compose
```sh
docker compose build
docker compose up -d
```

### 3️⃣ Acessar o container e interagir
```sh
docker exec -it webscraper_app /bin/sh
```

### 4️⃣ Rodar os testes
```sh
docker compose exec webscraper_app pytest --cov=.
```

### 5️⃣ Parar e limpar os containers
```sh
docker compose down
```

## 🛠️ Estrutura do Projeto
```
.
├── scrape
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── pyproject.toml
│   ├── poetry.lock
│   ├── tests/
│   ├── scrape/
│   │   ├── main.py  # Código principal
│   │   ├── utils.py  # Funções auxiliares
├── .github/workflows/ci.yaml  # CI/CD com GitHub Actions
└── README.md  # Documentação
```

## 📜 Licença
Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

