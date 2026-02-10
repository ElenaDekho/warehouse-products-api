# Склады и товары — REST API на DRF

CRUD API для управления товарами и складами с фильтрацией, поиском и пагинацией.

## Эндпоинты

### Товары
- `GET /api/v1/products/` — список товаров (пагинация по 3)
- `POST /api/v1/products/` — создать товар
- `GET /api/v1/products/{id}/` — детали товара
- `PUT /api/v1/products/{id}/` — обновить товар
- `DELETE /api/v1/products/{id}/` — удалить товар
- `GET /api/v1/products/?search=...` — поиск по названию/описанию (регистронезависимый)

### Склады
- `GET /api/v1/stocks/` — список складов (пагинация по 3)
- `POST /api/v1/stocks/` — создать склад с позициями товаров
- `GET /api/v1/stocks/{id}/` — детали склада с позициями
- `PUT /api/v1/stocks/{id}/` — обновить склад и позиции
- `DELETE /api/v1/stocks/{id}/` — удалить склад
- `GET /api/v1/stocks/?products=...` — фильтрация по id товара
- `GET /api/v1/stocks/?search=...` — поиск складов по названию/описанию товара

## Технологии
- Django 3.2.2
- Django REST Framework
- Django Filter (для поиска и фильтрации)
- SQLite (для разработки)

## Запуск
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver