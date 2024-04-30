# Ozon Parser
# Описание
Проект позволяет отправлять запросы для парсинга данных сохраняя их в бд и получать уведомление через телеграмм бота.
# Как запустить локально
- Я создал отдельного бота в телеграмме для этого проекта. Для начала нужно найти его по нику VoxWeb-test и написать ему /start
- Склонируйте репозиторий локально
- создайте и активируйте вертуальное окружение
```
python -m venv venv
source venv/Scripts/activate # Для Windows
source venv/bin/activate # Для MacOS, Linux
```
- Обновите pip и установите зависимости
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- Сделайте миграции
```
python manage.py makemigrations
python manage.py migrate
```
- запустите сервер после чего можете отправлять http запросы
```
python manage.py runserver
```
