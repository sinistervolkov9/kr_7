# kr_7

## Как пользоваться

### 1. Инструкция по запуску

Клонируйте проект на свой локальный компьютер

### 2. Установите Docker

Убедитесь, что Docker установлен на вашем устройстве. Скачать и установить Docker можно с официального сайта: [Docker Installation Guide](https://docs.docker.com/get-docker/).

### 3. Запустите контейнеры

Для запуска всех необходимых сервисов (Django, Celery, Redis, PostgreSQL) выполните команду:
docker-compose up -d --build

Эта команда соберет Docker-образы и запустит следующие сервисы:

- **web**: Django веб-сервер, доступный по адресу [http://localhost:8000](http://localhost:8000).
- **db**: Сервис PostgreSQL для хранения данных.
- **redis**: Redis для очередей задач.
- **celery_worker**: Celery worker для выполнения фоновых задач.
- **celery_beat**: Celery beat для планирования задач.
- **telegram_bot**: Запуск Telegram-бота

### 4. Примените миграции

Для настройки базы данных и применения миграций выполните:
docker-compose exec web python manage.py migrate

### 5. Создайте суперпользователя

Чтобы создать суперпользователя Django, выполните:
docker-compose exec web python manage.py csu

### 6. Доступ к приложению

- Django веб-приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).
- Админка Django будет доступна по адресу: [http://localhost:8000/admin](http://localhost:8000/admin).

### 7. Остановка

Чтобы остановить и завершить работу всех запущенных контейнеров, выполните команду:
docker-compose down

## Примечания

- Если у вас возникли проблемы с подключением к Redis, проверьте, что Redis работает правильно и доступен по адресу `localhost:6379`.
- Убедитесь, что все зависимости установлены в файле `requirements.txt`.
