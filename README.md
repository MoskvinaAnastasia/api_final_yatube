# api_final
# Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```git clone git@github.com:MoskvinaAnastasia/api_final_yatube.git```

```cd api_final_yatube```

- Cоздать и активировать виртуальное окружение:

```python -m venv venv```

- Если у вас Linux/macOS

```source env/bin/activate```

- Если у вас windows

```source venv/scripts/activate```

```python3 -m pip install --upgrade pip```

- Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```

- Выполнить миграции:

```python manage.py migrate```

- Запустить проект:

```python manage.py runserver```

- Готово, вы восхитительны
