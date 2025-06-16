# 📊 Term Frequency на Django

Веб-приложение для анализа загруженных текстовых файлов. Выполняет расчёт TF/IDF метрик, строит графики и сохраняет статистику обработки. Реализовано с использованием Django, PostgreSQL, Matplotlib и Docker.

---

## 🚀 Возможности

- ✅ Загрузка `.txt` файлов с автоматической проверкой формата
- 🔢 Подсчёт TF (term frequency) и IDF (inverse document frequency)
- 📈 Визуализация:
  - Топ-10 слов по TF
  - Топ-10 слов по IDF
  - Частотность слов
- 🧠 Сохранение статистики в базу данных (`FileMetric`)
- 🐳 Docker-окружение для лёгкого запуска
- 🧪 Метрики обработки файлов
- 📄 Swagger-документация для API

---

## ⚙️ Структура проекта

<pre><code>
Lesta/ 
├── base/                # Основное Django-приложение 
├── Lesta_task/          # Конфигурация проекта 
├── templates/           # HTML-шаблоны 
├── static/              # Статические файлы 
├── docs/                # Документация проекта 
│   └── database_structure.md  # Описание таблиц БД
├── db.sqlite3           # Локальная база (для отладки) 
├── .env                 # Переменные окружения 
├── Dockerfile           # Docker-образ 
├── docker-compose.yml   # Compose-конфигурация 
└── manage.py            # Django CLI 
</code></pre>

📄 [Описание структуры БД](docs/database_structure.md)

---

## 📘 Swagger API

Для просмотра доступных эндпоинтов — перейдите по ссылке:

[➡️ Swagger UI](http://localhost:8000/swagger/)

> Используется библиотека `drf-yasg`

---

## 🧪 Метрики

Метрики доступны по эндпоинту [`/metrics/`](http://localhost:8000/metrics/):

- `files_processed` — количество успешно обработанных файлов
- `min_time_processed`, `avg_time_processed`, `max_time_processed` — время обработки
- `latest_file_processed_timestamp` — время последнего успешного анализа

---

## 🐳 Запуск через Docker

1. Создай `.env`:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   APP_VERSION=1.2.3
   POSTGRES_DB=lesta_db
   POSTGRES_USER=lesta_user
   POSTGRES_PASSWORD=lesta_pass
   POSTGRES_HOST=db
   POSTGRES_PORT=5432

---
Changelog

## [1.2.3] - 2025-06-16
### Добавлено
- База данных на postgresql
- Функции входа, выхода, смены пароля
- Эндпоинты


## [1.1.3] - 2025-06-11
### Добавлено
- Метрики обработки файлов (min, max, avg time, timestamp)
- Вынесение переменных в `.env`
- База данных перенесена с `PostgreSQL` на `SQLite3`

## [1.1.2] - 2025-06-10
### Добавлено
- Эндпоинты `/metrics/`, `/version/`, `/status/`

## [1.0.0] - 2025-03-30
### Начало проекта
- Загрузка файлов
- Подсчёт слов и построение TF-графика
