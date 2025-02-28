# Проект "Contractor"

Проект предназначен для составления контрактов между бекендом и фронтендом. Это инструмент, который помогает стандартизировать взаимодействие между командами разработки, обеспечивая четкое описание API и требований.

**Статус проекта**: В разработке (фронтенд и бекенд активно дорабатываются).

---

## Оглавление

- [Установка и запуск](#установка-и-запуск)
- [Использование](#использование)
- [Технологии](#технологии)
- [Планы](#планы)
- [Лицензия](#лицензия)
- [Авторы](#авторы)
- [Благодарности](#благодарности)
- [Контакты](#контакты)

---

## Установка и запуск

Для запуска проекта локально необходимо использовать Docker и `docker-compose` и база данных `postgresql`.

1. Убедитесь, что у вас установлены [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).
2. Создайте пустую базу данных с именем `contractor`
```bash
createdb contractor
```
3. Создайте файл `.env`  в корневой директории проекта со следующим содержимым
```dotenv
# Секретный ключ Django (обязательно)(можно воспользоваться генератором(https://djecrety.ir))
SECRET_KEY=d^gsaxsd+3)(xzg*e4lpeam&zkol#@#lb!002&0+l6@dz^=+d8

# Режим отладки (prod или dev)
DEBUG=prod

# Настройки базы данных PostgreSQL
DB_USER=Имя пользователя вашей базы данных
DB_PASSWORD=Пароль вашей базы данных
DB_HOST=IP-адрес или хост вашей базы данных
DB_NAME=contractor
DB_PORT=Порт вашей базы данных (по умолчанию 5432)
```
4. Создайте файл `docker-compose.yml` в корневой директории проекта со следующим содержимым,
либо склонируйте репозиторий и используйте `docker-compose.yml` из репозитория:

```yaml
services:
  app:
    image: docker.tolq3.ru/contractor:main-latest
    command: >
      sh -c "python manage.py collectstatic --noinput && 
      python manage.py migrate && gunicorn contractor.wsgi:application --bind 0.0.0.0:8000"
    ports:
      - 8000:8000
    volumes:
      - ${PWD}/.env:/app/.env:ro

volumes:
  app-volume:
```
Либо можно использовать команды ```docker run -p 8000:8000 -v ${PWD}/.env:/app/.env docker.tolq3.ru/contractor:main-latest gunicorn contractor.wsgi:application --bind 0.0.0.0:8000```
5. Запустите проект с помощью команды:
```bash 
docker-compose up -d
```
6. После успешного запуска будет доступно:
 - Админ-панель по адресу http://localhost:8000/admin
 - Документация API по адресу http://localhost:8000/docs/swagger

7. Для создания супрепользователя используйте команду:
```bash
docker-compose exec -it app ./manage.py createsuperuser
```

## Использование

Проект предоставляет API для управления контрактами между бекендом и фронтендом. На данный момент доступны следующие функции:

- API для контрактов: Описание и управление контрактами(ведеться разработка и доработка).
- Swagger: Просмотр какие есть доступные конечные точки
- Админ-панель: На текущий момент пока что стандартная панель `Django-admin`

Так же доступна demo версия: [Admin](https://contractor.tolq3.ru/admin)

**login**: demo

**password**: 12345


Документация API: [Swagger](https://contractor.tolq3.ru/docs/swagger/) или [Redoc](https://contractor.tolq3.ru/docs/redoc/) 

Все что будет внесено в demo версии со временем может быть утерянно. Импользовать только для ознакомления

## Технологии

- **Backend**: Django, Django REST Framework
- **База данных**: PostgreSQL
- **Запуск**: Docker, Docker Compose
- **Документация API**: Swagger
- **Постановка задач**: YouTrack
- **CI/CD**: TeamCity

## Планы

* [ ] Сделать конечные точки для получения истории изменений контракта(версионирование)
* [ ] Добавить регистрацию и авторизацию через стороние сервисы(yandex, mail etc.)
* [ ] Продумать UI/UX, нарисовать дизайны
* [ ] Подружить бек и фронт

## Лицензия

Этот проект лицензирован под AGPL License

## Авторы

- Идея, бекенд, архитектура  - [Saimon](https://github.com/saimonq3)
- За фронтенд отвечает - [David](https://github.com/DAVIDhaker)

## Вклад в проект

Если вы хотите внести свой вклад в проект, пожалуйста, следуйте этим шагам:

- Создайте issue, чтобы обсудить предлагаемые изменения.
- Сделайте fork репозитория и создайте новую ветку для ваших изменений.
- Отправьте pull request с описанием ваших изменений.
- Предложить свои идеи можно в в обратной связи в [YouTrack](https://yt.tolq3.ru/form/4caa593a-d6c0-4f00-beac-1f394f8719fc)


Мы рады любым предложениям и улучшениям!

## Благодарности

- Спасибо [David](https://github.com/DAVIDhaker) за согласие и помощь в разработке фронтенда

## Контакты

Если у вас есть вопросы или предложения, свяжитесь с нами:

- Email: [saimonq3@gmail.com](mailto:saimonq3@gmail.com)
- Telegram: [@saimonq3](https://t.me/saimonq3)