По-русски | [In english](docs_eng/README.md)
# Скрипт публикации комиксов в сообществе ВКонтакте
Публикует случайный комикс с сайта ``https://xkcd.com/`` 


### Как использовать?
Python3 должен быть уже установлен.

Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей.
Открываем командную строку клавишами Win+R и вводим:
```commandline
pip install -r requirements.txt
```
Рекомендуется использовать virtualenv/venv для изоляции проекта.
(https://docs.python.org/3/library/venv.html)



### Настройка переменных окружения

До запуска необходимо создать файл ".env" в папке ПУТЬ_К_ПАПКЕ_СО_СКРИПТОМ\
и настроить переменные окружения, прописав в нем:
```
VK_ACCESS_TOKEN=Ваш токен в ВК
```
инструкция, по Implicit Flow для получения ключа доступа пользователя ВК
```
https://vk.com/dev/implicit_flow_user
```

```
VK_GROUP_ID=ID созданного Вами сообщества ВК
```
записан в настройках ("Управление") сообществом (нужны только цифры)


### Как использовать?

Команда на запуск скрипта для размещения случайного комикса в ВК:
```commandline
python main.py
```


### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
