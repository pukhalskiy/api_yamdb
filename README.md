# Встречайте платформу YaMDb !
## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
***
## Технологии
Python 3.7
Django 2.2.19
***

## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ArseniyAngel/api_yamdb.git
```

```
cd api_yamdb/
```

### Cоздать и активировать виртуальное окружение:
#### Для Windows
```
python -m venv env
```
```
venv\Scripts\activate.bat
```
#### Для Linux и MacOS
```
python3 -m venv venv
```
```
source env/bin/activate
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:
**!Не забудьте перейти в папку с файлом manage.py!**
#### Для Windows
```
python manage.py migrate
```
#### Для Linux и MacOS
```
python3 manage.py migrate
```

### Запустить проект и Dev-режиме:
#### Для Windows
```
python manage.py runserver
```
#### Для Linux и MacOS
```
python3 manage.py runserver
```
***
## Примеры запросов к API:
### **Авторизация:**
### Регистрация нового пользователя
```
http://127.0.0.1:8000/api/v1/auth/signup/
```
### Получение JWT-токена
```
http://127.0.0.1:8000/api/v1/auth/token/
```
***
### **GET**
### Получение списка всех категорий
```
http://127.0.0.1:8000/api/v1/categories/
```

### Получение списка всех жанров
```
http://127.0.0.1:8000/api/v1/genres/
```
### Получение списка всех произведений
```
http://127.0.0.1:8000/api/v1/titles/
```

### Получение информации о произведении
```
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```

### Получение списка всех отзывов
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
### Получение отзыва по id
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
```

### Получение списка всех комментариев к отзыву
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

### Получение комментария к отзыву
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```
***
### **POST**
 **Пользователи должны быть аутентифицированны**
### Добавление нового отзыва
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

### Добавление комментария к отзыву
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
***
## Подробнее можно узнать запустив Dev-сервер и перейдия по адресу 
```
http://127.0.0.1:8000/redoc
```
***

## Авторы
**Разумов Арсений, Наталья Арлазарова, Егор Пухальский и команда Яндекс.Практикума**
