# Дз 4. Веб сервис.
Это мини-дашборд с CRUD-операциями для данных по энергопотреблению и ценам. 

## Проект
Бэкенд на FastApi
Фронт на Streamlit

Проект поддерживает получение данных из CSV файла, выдачу их, добавление новых записей и удаление по ID
Фронт получает данные по API и отображает таблицу и графики. 

структура:

'''text
task_04_service/
    backend
        main.py
        data.csv
    frontend
        app.py
    README.md
    requirements.txt

'''

Используемые технологии :
Python
FastAPI
Streamlit
Pandas
Plotly
Requests
Uvicorn
Pydantic

## Проект также развернут на Render
Ссылка :

## Установка

Создайте и активируйте виртуальное окружение.

Windows
'''bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
'''
Linux / macOS
'''bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
'''

Запускаем бэк и фронт из корня проекта в разных терминалах
```
uvicorn backend.main:app
```
```
streamlit run frontend/app.py
```

Фронт будет доступен по адресу:
http://localhost:8501
Документация по:
http://127.0.0.1:8000/docs

## API

GET /records — получить все записи

POST /records — добавить новую запись

DELETE /records/{id} — удалить запись по id

## Итог
Таким образом, приложение выполняет все критерии выполнения дз, а именно:
README.md с инструкцией по запуску
Backend API
UI: отображение данных (графики и т.д.)
UI: операции через API (POST/DELETE) 
Статусы и коды ответов HTTP
Персистентность данных после работы с API
Валидация через Pydantic 
Обработка ошибок
Деплой в Streamlit Cloud / Render 
