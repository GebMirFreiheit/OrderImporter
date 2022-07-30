**OrderImporter**

Проект выполнялся в качестве тестового задания

OrderImporter представляет собой простое одностраничное приложение на Django. По адресу `0.0.0.0:8000/orders/` находится таблица с заказами, которые присутствуют в базе данных. Когда приложение запущено, раз в минуту подтягиваются изменения из Google-таблицы с заказами и в соответствии с этим из базы данных удаляются неактуальные заказы, изменяются старые или добавляются новые. Также при импорте данных из таблицы заказу добавляется новое поле, стоимость в рублях. При обновлении информации совершается запрос к api центробанка, чтобы корректно перевести стоимость в долларах в стоимость в рублях.

**Подготовка и запуск**
Для запуска проекта необходимо, чтобы в системе был установлен Python версии не ниже python3.7 и Docker Compose. Проверяющему, у которого есть доступ к таблице, необходимо поместить JSON файл со своим ключом в папку проекта, переименовав файл в `credentials.json`. В файл `.env` нужно записать данные для доступа к базе данных (название, имя пользователя и пароль) в формате VAR=VAL. Чтобы собрать проект, нужно выполнить команду `docker-compose --build`. Будут созданы два docker контейнера, для PostgreSQL базы данных и для сервиса на Django. Чтобы в базе данных была создана таблица для заказов, необходимо выполнить команду `docker exec -it order_importer_web_1 python manage.py migrate`. После этого можно начинать работу с сервисом.

**Как выполняются периодические задачи**
Ежеминутное обновление таблицы заказов реализовано с помощью библиотеки schedule и перегрузки метода ready у приложения. При запуске приложения создаётся подпроцесс, в котором каждую минуту отрабатывает функция запроса к Google таблице. Я сочла, что для небольшой задачи это достаточно приемлемое решение. При необходимости добавлять больше периодических задач можно перевести проект на Celery.

**Примечания**
Для удобства тестирования в коде оставлен Django secret key, также ссылка на Google таблицу захардкожена. При использовании в продакшене Django secret key и ссылку на таблицу стоит вынести в переменные окружения. Также необходимо добавить более строгую валидацию входных данных.