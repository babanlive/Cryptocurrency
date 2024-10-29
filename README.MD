# Асинхронный клиент и API для получения информации о текущем курсе криптовалюты с криптобиржи Deribit.

## Описание проекта

Проект представляет собой веб-приложение, которое реализует асинхронный клиент для криптобиржи Deribit. Клиент каждую минуту получает актуальные цены на BTC и ETH (индексные цены) и сохраняет их в базе данных. для обработки и предоставления доступа к сохранённым данным реализован REST API на FastAPI.

## Функциональность

- Получение текущих цен для BTC и ETH.
- Сохранение цен в базу данных с указанием тикера, цены и времени в формате UNIX timestamp.
- API для работы с сохранёнными данными:
  - Получение всех сохранённых данных по указанной валюте.
  - Получение последней цены указанной валюты.
  - Получение цен с фильтром по дате.

## Технологии и инструменты

- Python 3.12
- FastAPI
- aiohttp
- SQLAlchemy
- PostgreSQL
- Docker

## Установка и запуск проекта

1. Клонируйте репозиторий и перейдите в папку проекта:

    ```shell
    git clone https://github.com/babanlive/Cryptocurrency.git && cd Cryptocurrency
    ```

2. Создайте файл `.env` в папке приложения (fastapi-application) согласно образцу [.env_example](fastapi-application/.env.example).

3. Запустите проект через Docker:

  - Для запуска в режиме разработки выполните команду:

    ```shell
    docker compose -f docker-compose.yaml up --build
    ```

4. Выполните миграции:

    ```shell
    docker exec -it app_fastapi poetry run alembic upgrade head
    ```

## Работа с API

### Базовый URL

API доступно по адресу:

```shell
http://127.0.0.1:8000/api/v1/
```

### Документация API доступна в формате Swagger по следующему адресу:

```shell
http://127.0.0.1:8000/docs
```

### Запросы к API:

 - GET /prices/tickers — Получение всех сохранённых данных по указанной валюте.
 - GET /prices/tickers/latest — Получение последней цены указанной валюты.
 - GET /prices/tickers/date — Получение цен указанной валюты с фильтром по дате.


### Примеры запросов
1. Получение всех сохранённых данных для тикера BTC_USD:

    ```shell
      curl -X 'GET' \
      'http://127.0.0.1:8000/api/v1/prices/tickers?ticker=BTC_USD' \
      -H 'accept: application/json'
    ```

2. Получение последней цены для тикера ETH_USD:
    ```shell
      curl -X 'GET' \
      'http://127.0.0.1:8000/api/v1/prices/tickers/latest?ticker=ETH_USD' \
      -H 'accept: application/json'
    ```

3. Получение цен для тикера BTC_USD с фильтром по дате:

    ```shell
      curl -X 'GET' \
      'http://127.0.0.1:8000/api/v1/prices/tickers/date?ticker=BTC_USD&date=2024-10-27' \
      -H 'accept: application/json'
    ```

## Тесты
1. Создайте тестовую БД

    ```shell
    docker exec -it pg_db psql -U user -d postgres -c "CREATE DATABASE test_db;"
    ```

2. Запустите тесты:

    ```shell
    docker exec -it app_fastapi poetry run pytest -v tests/ --disable-warnings
    ```
