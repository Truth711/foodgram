# Продуктовый помощник Foodgram 

## Описание:
Сервис позволяет пользователям постить свои кулинарные рецепты
и просматривать уже существующие рецепты. Рецепты отсортированы по тегам.

 Пользователи имеют возможность
подписаться на любимого автора, добавить понравившийся рецепт в избранное
и в список покупок, который затем могут скачать в виде pdf-файла.

Регистрация и авторизация реализованы с использованием authtoken. 

Проект упакован в три docker-контейнера.

Фронтенд реализован с использованием React.js
## Технологии:
- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Docker](https://www.docker.com)
- [Docker-compose](https://docs.docker.com/compose/)
- [PosgreSQL](https://www.postgresql.org)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org)

## Установка и развертывание проекта:
- Клонировать репозиторий, перейти в директорию с проектом
- Создать виртуальное окружение и установить зависимости из requirements.txt
- Установить Docker и docker-compose
- Забилдить и поднять проект:
```
$ docker-compose up -d --build 
```
- Выполнить команды для миграции, создания суперюзера и сбора статики:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```
- Загрузить список ингредиентов из фикстуры:
```
docker-compose exec web python manage.py loaddata ingredients.json
```
- Готово!
