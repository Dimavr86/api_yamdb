# Описание сервиса «API для Yatube»

Предоставляет API со следующими возможностями:
1. Работа с публикациями:
	- Получение списка всех публикаций (с возможностью распределения по страницам).
	- Получение, создание, полное или частичное обновление отдельной публикации.
2. Работа с комментариями:
    - Получение комментариев к публикации.
	- Получение, создание, полное или частичное обновление отдельного комментария.
3. Работа с сообществами:
    - Получение списка всех сообществ.
    - Получения сведений об конкретном сообществе.
4. Работа с подписками:
    - Получение списка подписчиков пользователя.
    - Подписаться на конкретного пользователя.
5. Работа с JWT-токеном:
    - Получение.
    - Обновление.
    - Проверка.

Более подробные сведения: http://localhost:8000/redoc/.

***

## Установка и настройка

1. Клонируйте репозиторий в свою рабочую директорию на компьютере:

```
git clone https://github.com/Filin888/api_final_yatube.git
```

2. Создайте и активируйте виртуальное окружение, установите все необходимые пакеты:


```
cd /d/Dev/api_final_yatube
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install django-filter
```

3. Создайте и примените миграции:

```
cd yatube_api
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

6. Действия по настройке сервиса API завершены!

## Примеры использования

### Получаем токен.

1. В административной панели приложения создаем пользователя `http://127.0.0.1:8000/admin/auth/user/add/`. Для этого понадобятся права супер-пользователя, который был создан ранее.

2. Для доступа к API вновь созданному пользователю необходи токен. Отправляем POST-запрос на `http://127.0.0.1:8000/api/v1/jwt/create/` с полями в секции 'data'
- имя пользователя - укажите имя пользователя.
- пароль - укажите пароль пользователя.
После этого API вернет основной и аварийный токены:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NjUzNzYwOCwianRpIjoiYTM5MDU2M2Q0ZTVmNDFkMThlN2UzNGEwYWEyOWIzOTQiLCJ1c2VyX2lkIjoyfQ.EhKX6RK2RoxVfemmztgkzqVa5gmDvyiafkjVGzxznwQ",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2NTM3NjA4LCJqdGkiOiIxMGM0Y2QwYTE1ZjQ0NjNjOTMzYTdlOWM0MWI5ZGU3NCIsInVzZXJfaWQiOjJ9.9WW-FqVmrF4l5S7ayjJnnm2r1d5cFveF0DKmApapmCw"
}

"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2NTQwMDc3LCJqdGkiOiI0MjdmMjc2MTU3YmM0MDVkYTMyN2RlNjU2YjkzZDExMCIsInVzZXJfaWQiOjJ9.sR9jU8VxAoHC5wf95W8x2IS5_VUx8v0GKD-fou9nQJA"
Основной токен необходим для выполнения операций с изменением данных, аварийный токен нужен для обновления/восстановления основного. Пользователь должен хранить в секрете свои токены.

### Создание публикации
Отправляем POST-запрос на `http://127.0.0.1:8000/api/v1/posts/` с параметром `text`, который является содержанием новой публикации. Для этого запроса понадобится созданный ранее токен пользователя.

### Просмотр публикации
Отправляем GET-запрос на `http://127.0.0.1:8000/api/v1/posts/` и получае список всех публикаций.





