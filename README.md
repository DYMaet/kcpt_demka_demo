Демка для демки.
Логинопароль для админа задаётся при запуске python manage.py createsuperuser или django-admin createsuperuser
Запускается простым python manage.py runserver
Для работы нужен только django:
pip install django
Также перед первым запуском надо выполнить миграции ну и соответственно создать суперюзера.
ВЕСЬ ПРОЦЕСС ПЕРВОГО ЗАПУСКА:
Находясь в папке demkaisip2 в powershell или cmd прописываем
python manage.py makemigrations demka
python manage.py migrate
python manage.py createsuperuser
вводим логин пароль почту (почту любую, она не используется) и прочее что требуется. По заданию это Admin KorokNET
python manage.py runserver - запуск сервера
