# API Yamdb
### API Yamdb - Проект для размещения отзывов о фильмах, книгах и музыке. 
### Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Использованные технологии:
- Python 3.9,
- Django 3.2,
- Django Rest Framework 3.12
- JWT

Ресурсы API YaMDb:
- auth: аутентификация пользователей и получение jwt-токена для работы с сервисом.
- users: пользователи. Список может быть получен только администратором. 
- titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Как пользоваться API?
Клонируем репозиторий:
```python
git clone https://github.com/Amir800S/api_yamdb.git
```
Создаем и активируем виртульное окружение в терминале:
```python
python -m venv venv
```
```python
venv/Scripts/activate
```
Далее установка зависимостей:
```python
pip install -r requirements.txt
```
Запускаем сервер:
```python
python manage.py runserver
```
### Проект готов к работе
## К проекту подключена автоматическая документация drf-spectacular со всеми эндпоинами и примерами запросов.
```python
http://127.0.0.1:8000/schema/redoc/
```
## * Примеры отправки GET-запросов к API:
```python
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  # Получение списка всех отзывов
http://127.0.0.1:8000/api/v1/titles/  # Получение списка всех произведений
http://127.0.0.1:8000/api/v1/titles/{titles_id}/  # Получение информации о произведении
```
### * Примеры создания пользователя и аутентификации: 
POST-запрос регистрации пользователя
```python
http://127.0.0.1:8000/api/v1/auth/signup/
```
```python
{
  "email": "user@example.com",
  "username": "string"
}
```
Пример ответа с 201-кодом, пользователь создан и на указанный email отправлено сообщение
```python
{
{
  "email": "string",
  "username": "string"
}
```
## Как получить `JWT-токен`?
POST-запрос с кодом подтверждения указанным в email
```python
http://127.0.0.1:8000/api/v1/auth/token/
```
В Payload:
```python
{
  "username": "string",
  "confirmation_code": "string"
}
```
Токен получен! 
```python
{
  "token": "string"
}
```
## ***Над проектом работали:***
### ⫸ [*Амир Сосламбеков*](https://github.com/Amir800S) 
### ⫸ [*Нурбек Орозалиев*](https://github.com/Nurbek878) 
### ⫸ [*Михаил Ашин* ](https://github.com/MichaelAshin)
### ⫸ [*Михаил Ашин* ](https://github.com/MichaelAshin)
