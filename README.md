# Описание сервиса «API_YaMDB»

Сервис API для YaMDB собирает отзывы (Review) и оценки пользователей на произведения (Title) в разных категориях и жанрах, а так же комментарии к отзывам. Произведения делятся на категории (Category) и жанры (Genres), список которых может быть расширен, но правами на добавление новых жанров, категорий и произведений обладает только администратор. Для авторизации пользователей используется код подтверждения.Для аутентификации пользователей используются JWT-токены.

Ресурсы сервера:
```
Аутентификация: /api/v1/auth/token/
Работа с пользователями: /api/v1/users/
Перечень произведений: /api/v1/titles/
Жанры произведений: /api/v1/genres/
Категории произведений: /api/v1/categories/
Отзывы на произведения: /api/v1/titles/{title_id}/reviews/
Комментарии к отзывам: /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
Пользователи и роли:
```
Аноним — обладает только правами просмотра.
Аутентифицированный пользователь (user) — помимо прав Анонима, публикует отзывы и оценки произведений, комментирует отзывы, редактирует и удаляет свои отзывы и комментарии. 
Модератор (moderator) — помимо прав Аутентифицированного пользователя, удалятет любые отзывы и комментарии.
Администратор (admin) — полные права на управление всеми записями.
Суперюзер Django — обладет правами администратора на уровне Django.
```
***

## Установка и настройка

1. Клонируйте репозиторий в свою рабочую директорию на компьютере:

```
git clone https://github.com/Dimavr86/api_yamdb.git
```

2. Создайте и активируйте виртуальное окружение, установите все необходимые пакеты:

```
cd /d/Dev/api_yamdb
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install django-filter
pip install djoser djangorestframework_simplejwt 
```

3. Создайте и примените миграции:

```
cd api_yamdb
python manage.py makemigrations
python manage.py migrate
```

4. Создайте супер-пользователя:

```
winpty python manage.py createsuperuser
```

5. Запустите тестовый сервер:

```
python manage.py runserver
```

6. Действия по настройке сервиса завершены!

## Примеры использования

### Регистрация пользователей.

1. Пользователь отправляет POST-запрос эндпоинт /api/v1/auth/signup/ с параметрами:
```
{
  "email": "string",
  "username": "string"
}
```
2. В ответ сервис прислылает на указанный адрес email письмо с кодом подтверждения (confirmation_code).

3. Пользователь отправляет POST-запрос с на эндпоинт /api/v1/auth/token/ с параметрами:
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
4. В ответ сервис прислылает token (JWT-токен):
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NjUzNzYwOCwianRpIjoiYTM5MDU2M2Q0ZTVmNDFkMThlN2UzNGEwYWEyOWIzOTQiLCJ1c2VyX2lkIjoyfQ.EhKX6RK2RoxVfemmztgkzqVa5gmDvyiafkjVGzxznwQ"
}
```

### Работа с API для авторизованных пользователей:

Добавление категории (для Администраторов):
```
POST /api/v1/categories/
{
  "name": "string",
  "slug": "string"
}
```
Удаление категории (для Администраторов):
```
DELETE /api/v1/categories/{slug}/
```
Добавление жанра:

Права доступа (для Администраторов):
```
POST /api/v1/genres/
{
  "name": "string",
  "slug": "string"
}
```
Удаление жанра (для Администраторов):
```
DELETE /api/v1/genres/{slug}/
```
Обновление публикации (для Администраторов):
```
PUT /api/v1/posts/{id}/
{
	"text": "string",
	"image": "string",
	"group": "string"
}
```
Добавление произведения:

Права доступа (для Администраторов):
```
POST /api/v1/titles/
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
Добавление произведения (для Анонимов)
```
GET /api/v1/titles/{titles_id}/
{
  "id": int,
  "name": "string",
  "year": int,
  "rating": int,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
Обновление сведений о произведении (для Администраторов):
```
PATCH /api/v1/titles/{titles_id}/
{
  "name": "string",
  "year":  "string",
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```


