###Элементарный пример реализации интернет-магазина (Flask+SqlAlchemy+Bootstrap)

Для запуска проекта на машине должны быть установлены docker и docker-compose

Для разработки требуется python версии не ниже 3.6 

####Быстрый запуск.

В файле docker-compose.yml измените путь, по которому будут храниться файлы MySQL, а также пароль пользователя (по желанию):
```yaml
services:
  database:
    ...
    environment:
      MYSQL_ROOT_PASSWORD: <your_password>
    ...
    volumes:
      - ./init.sql:/data/application/init.sql
      - /path/to/data:/var/lib/mysql
```
выполните команду в папке проекта:
```bash
docker-compose up --build -d
```
и дождитесь запуска всех контейнеров

После запуска будут доступны:

http://localhost:7890 - стартовая страница магазина

http://localhost:8765 - стартовая страница phpMyAdmin, подключенный к серверу MySQL

Изначально не имеется категорий и самих товаров, их можно добавить перейдя по ссылке 

http://localhost:7890/admin 

Для остановки всех компонентов проекта и удаления созданных контейнеров выполните в папке проекта команду:
```bash
docker-compose down
```

Все данные по добавленным продуктам и категориям будут сохранены в базе, и после перезапуска проекта будут доступны снова.

####Разработка

Для выполнения разработки можно поднять отдельно сервер MySQL командой:
```bash
docker run -d --restart always -e MYSQL_ROOT_PASSWORD=12345 -v /path/to/data:/var/lib/mysql --name mysqlserver mariadb
```
Узнать адрес сервера MySQL можно командой:
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysqlserver
```
Полученный адрес указать в файле config.py:
```python
db_host = env.get('DB_HOST', '172.17.0.2')
```
или выставить с помощью указанной выше команды переменную окружения DB_HOST

[alt text](./screenshots/index.png)

[alt text](./screenshots/admin.png)
