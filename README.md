# QRkot_spreadseets
## Приложение QRKot — это приложение для Благотворительного фонда поддержки котиков. 
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
## Ключевые возможности сервиса
- В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
- Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
- В приложении есть возможность формирования отчёта в гугл-таблице. В таблице показываются закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Стек технологий
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Asyncio
- Google API
## Команды для развертывания
```
git clone https://github.com/opzhai/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Обновить библиотеку pip, установить зависимости

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Создать файл .env и заполнить его по следующему шаблону:
```
APP_TITLE=QRKot 
APP_DESCR=Благотворительного фонда поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db 
SECRET=fjednfsvlkdnvljdsnf
FIRST_SUPERUSER_EMAIL=admin@mail.ru
FIRST_SUPERUSER_PASSWORD=admin
# адрес вашего личного гугл-аккаунта
EMAIL=
# данные из JSON-файла с информацией для авторизации приложения в сервисном аккаунте
TYPE="service_account"
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url="https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url=
```
Применить миграции для создания БД
```
alembic upgrade head
```
Запустить проект:

```
uvicorn app.main:app
```
Документация к API будет доступна по следующим адресам:

http://127.0.0.1:8000/docs - Swagger

http://127.0.0.1:8000/docs - ReDoc


## Автор
[Александр Позжаев](https://github.com/opzhai/) <a href='https://github.com/opzhai/'>