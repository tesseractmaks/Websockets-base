# Урок 4. Подключаемся к подпольному чату

Две консольные программы — одна читает сообщения, другая их отправляет.

## Установка

Для запуска программы потребуется предустановленный Python 3.8+ 

Скопировать репозиторий в текущий каталог можно командой:
```
$ git clone https://github.com/tesseractmaks/Websockets-base.git
```



## Запуск

Перейти в каталог с программой:
```
$ cd Websockets-base
```
Установите зависимости:

```
$ python3 pip install -r requirements.txt
```

Запуск программы чтения сообщений:
```
$ python3 main.py
```

#### Аргументы
- Используйте флаг для ввода хоста: **-ht** или **--host**
- Используйте флаг для ввода порта: **-p** или **--port**
- Используйте флаг для указания пути до файла с логами: **-ph** или **--path**
- Используйте флаг для вызова помощи: **-h** или **--help**

Запуск программы отправки сообщений:
```
$ python3 sender.py
```

#### Аргументы
- Используйте флаг для регистрации: **-r** или **--reg**
- Используйте флаг для аутентификации: **-t** или **--token**
- Используйте флаг для ввода хоста: **-ht** или **--host**
- Используйте флаг для ввода порта: **-p** или **--port**
- Обязательный аргумент сообщения: **msg**
- Используйте флаг для вызова помощи: **-h** или **--help**


**Пример команд:**

```python
$ python3 sender.py -r <username> <сообщение>
```

```python
$ python3 sender.py -t <token> <сообщение>
```


## Автор

**vlaskinmac**  - [GitHub-vlaskinmac](https://github.com/vlaskinmac/)

# Цели проекта

Код написан в образовательных целях.
