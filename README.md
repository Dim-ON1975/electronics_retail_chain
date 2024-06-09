# Проект "Тестовое задание для старта трудоустройства № 1"
##  Модель сети по продаже электроники
### Заберов Дмитрий (zaberov.dv@internet.ru), Python IND 27.0

### Описание
Данная работа представляет собой разработку онлайн платформы торговой сети электроники.
Убедиться в работоспособности сайта, развёрнутого на локальном компьютере посредством Docker:
 - app:
   - административная панель: http://localhost:8000/admin/
   - документация swagger (OpenAPI 2): http://localhost:8000/api/swagger/
   - документация redoc: http://localhost:8000/api/redoc/
   - от документирования на drf-specicular (OpenAPI 3) пришлось отказаться из-за громоздкого кода.

## Функционал
1. Авторизация и аутентификация пользователей.
2. Распределение ролей между пользователями (пользователь и админ).
3. CRUD для продуктов.
4. CRUD для поставщиков.

## Технологии
1.  Python 3.11.
2.  Django 4.2.13.
3.  Django REST framework 3.15.1.
4.  django-filter 24.2.
5.  psycopg2-binary 2.9.9.
6.  JWT 5.3.1.
7.  DRF-YASG 1.21.7.
8.  Djoser 2.2.2.
9.  Docker 26.1.4.
10. Docker Compose v2.27.1-desktop.1


## Использование
Проект "Electronics Retail Chain" представляет собой веб-приложение для управления розничной сетью электроники. Здесь вы найдете функционал для управления товарами и поставщиками вашей электронной розничной сети.
![users.png](image_readme/users.png)
![products.png](image_readme/products.png)
![suppliers.png](image_readme/suppliers.png)
![suppliers-form.png](image_readme/suppliers-form.png)
![suppliers-from-1.png](image_readme/suppliers-form-1.png)
![suppliers-form-2.png](image_readme/suppliers-form-2.png)

## Тестирование
1. Настройки в файле **.coveragerc**
2. Из директории проекта запустить команду тестирования `python manage.py test`
3. После успешного прохождения тестов запустить следующие команды для формирования отчёта(-ов):
    - запуск тестов конкретных приложений с выводом подробностей тестирования: `coverage run --source='products,suppliers,users'  manage.py test -v 2`
    - вывод результатов тестирования в виде отчёта в терминал: `coverage report --skip-covered`
    
    <p align="center"><img src="image_readme/test-report.png" width="500"></p>
    - вывод результатов тестирования в виде html-отчёта: `coverage html --skip-covered`
    
    <p align="center"><img src="image_readme/html-report.png" width="500"></p>


### **Установка**
Для установки проекта, следуйте инструкциям, указанным ниже:

1. Сделайте Fork этого репозитория. Клонируйте форкнутый репозиторий, чтобы получить его локально.

2. Перейдите в директорию проекта.

3. Создайте и активируйте виртуальное окружение:</p>

   `poetry init`
   
   `poetry shell`

4. Установите зависимости проекта (зависимости, необходимые для установки, можно найти в файле **pyproject.toml**):

   `poetry install`

5. Создайте файл **.env** в корневой папке проекта и заполните данные для настройки проекта из файла **.env.sample**
6. В директории создайте дерево каталогов **persistentdata/**, как показано на иллюстрации ниже:

<p align="center"><img src="image_readme/persistentdata.png" width="200"></p>

Все остальные настройки указаны в **Dockerfile**, docker-compose.yaml**, **nginx/default.conf**. Для запуска проекта достаточно запустить **docker-compose.yaml** из корня проекта, о чём написано ниже.

### Требования
Для запуска проекта в Docker необходимо:
- выполнить команду `docker-compose up --build`

_или_
- последовательно выполнить команды:
  - собрать образ: `docker-compose build`
  - запустить контейнеры: `docker-compose up`

### Дополнительно
Следует учитывать, что настройки вынесены в файл .env, который не выкладывается в репозиторий, однако имеется файл **.env.sample**, позволяющий разработчику определить перечень необходимых ключей и настроек для работы приложений.

Полезные команды для перезапуска процесса контейнеризации:
- Очистка тома: `docker volume prune -f`
- Удалить всё и сразу без подтверждений: `docker system prune -af`

Полезные команды для получения доступа к контейнеру, содержащему проект:
- Запуск командной оболочки: `docker-compose exec app bash`
- Активация виртуального окружения в контейнере: `source env/bin/activate`

## Особенности
### Проект содержит несколько приложений:
1.  users – приложение для регистрации и авторизации пользователей проекта посредством Djoser (информацию по **users.urls** см. ниже).
2.  products – приложение для продуктов, включающие операции создания, просмотра, редактирования и удаления (CRUD).
3.  suppliers – приложение для поставщиков, включающие операции создания, просмотра, редактирования и удаления (CRUD).

### Технические особенности:
1. Для разных сервисов созданы отдельные контейнеры (db - postgresql, app - django, nginx - nginx).
2. Проект имеет следующий функционал:
   - Авторизация и аутентификация пользователей посредством Djoser. Письма при авторизации (активации), изменении электронной почты, пароля, сбросе, восстановлении пароля приходит на указанную почту с соответствующими ссылками. Пример письма, отправляемого при авторизации (активации пользователя)
   ![user-activation.png](image_readme/user-activation.png)
   - Распределение ролей между пользователями (пользователь и админ), для чего используются необходимые permissions.
   - Реализовано восстановление пароля через электронную почту.
   - CRUD для товаров на сайте (админ может удалять или редактировать все товары, а пользователи только свои).
   - CRUD для поставщиков на сайте (админ может удалять или редактировать всех поставщиков, а пользователи только своих).
     Сеть представляет собой иерархическую структуру из трех уровней:
     - завод;
     - розничная сеть;
     - индивидуальный предприниматель.
     Каждое звено сети ссылается только на одного поставщика оборудования. Уровень иерархии определяется не названием звена, а отношением к остальным элементам сети, т. е. завод всегда находится на уровне 0, а если розничная сеть относится напрямую к заводу, минуя остальные звенья, ее уровень — 1.
   - В админ-панели поставщиков добавлены:
     - ссылка на «Поставщика»;
     - цепочка поставщиков, содержащая ссылки на поставщиков цепочки;
     - фильтры, в т.ч. по названию города;
     - admin action, очищающий задолженность перед поставщиком у выбранных объектов;
   - В админ-панелях пользователей и товаров добавлены вычисляемые поля для отображения миниатюр изображений (превью аватаров пользователей и товаров).

### Установка зависимостей
Зависимости, необходимые для работы и тестирования проекта указаны в **pyproject.toml**.

### Справочные данные по users.urls

1. **POST jwt/create/?** [name='jwt-create'] - получение refresh и access токенов jwt
   
         запрос: email, password.
            
         результат: refresh и access токены jwt, например:
         
         {
             "refresh": "eyJhbGciOiJIUzI1NiIs...2E3MiIsInVzZXJfaWQiOjF9.DPUiIbzKHRYiscM0dxGxryox_6YwYV899eKu0jFBmJU",
             "access": "eyJhbGciOiJIUzI1NiIsI...ODk2IiwidXNlcl9pZCI6MX0.h-ZFeFyttJs7dE7al6sDM_s8nAc-UbhLoXspeOMenpU"
         }

2. **POST jwt/refresh/?** [name='jwt-refresh'] - обновление jwt-токенов.

         запрос: refresh-токен, например:
      
         {
             "refresh": "eyJhbGciOiJIUzI1NiIsInR5c...IsInVzZXJfaWQiOjF9.kGVNN3IqgJ4GqFd5GqwVBF0tft6Zly9yt3n-o5qkf6o"
         }
      
         результат: access-токен, например:
      
         {
             "access": "eyJhbGciOiJIUzI1NiIsI...MWFhIiwidXNlcl9pZCI6MX0.6ypUqk65Uv9agbEq-KEaxu_7sdfKvvWHu5ccAcNGqs0"
         }

3. **POST jwt/verify/?** [name='jwt-verify'] - проверка jwt-токенов

         запрос: token (refresh или access), например:
         
         `{
             "token": "eyJhbGciOiJIUzI1NiIsIn...NGMwIiwidXNlcl9pZCI6MX0.sklX78DpWjrObyONhPDFmfIs5m1HMQhO3qmRxxtWKpY"
         }`
         
         результат: {} status 200 OK, если с токеном всё в порядке.

4. **POST users/$** [name='users-list'] - CREATE - регистрация пользователя:

         запрос: email, password, re_password

         результат: регистрация пользователя, отправка письма со ссылкой для активации на почту (сейчас is_active=False)

5. **GET users/$** [name='users-list'] - READ - список профилей пользователя:

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4
         
         результат: данные профиля

6. **POST users/activation/$** [name='users-activation'] - активация пользователя по ссылке из письма:

         запрос: из ссылки в письме, например, http://127.0.0.1:8000/users/activation/Mw/c6wush-4a905a7e9c07811b3da72801dd7b5c88
         
         uid: Mw, token: c6wush-4a905a7e9c07811b3da72801dd7b5c88
         
         результат: пользователь активирован - is_active=True

   **Внимание!** После активации нужно сгенерировать токен для пользователя **'/auth/token/login/'**, иначе на следующих шагах авторизации вы получите ошибку.

7. **GET users/me/$** [name='users-me'] - READ - получение своего профиля:

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4 
         
         результат: данные профиля

8. **PUT, PATCH users/me/$** [name='users-me'] - UPDATE - полное (PUT) или частичное (PATCH) изменение своего профиля:

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4
      
         результат: изменение данных профиля (доступны для изменения все поля)

9. **GET users/{id}/$** [name='users-detail'] - READ - просмотр профиля пользователя (USER - свой, ADMIN - любой)

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4
         
         результат: данные отдельного пользователя

10. **PUT, PATCH users/{id}/$** [name='users-detail'] - UPDATE - полное (PUT) или частичное (PATCH) пользователя (USER - свой, ADMIN - любой)

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4
         
         результат: изменение данных профиля (доступны для изменения: "id", "email", first_name", "last_name", "phone", "role")

11. **DELETE users/{id}/$** [name='users-detail'] - DELETE - удаление пользователя (USER - свой, ADMIN - любой)

         запрос: email, password, headers: Authorization: Token 0944e011ae67e1a7e9b19a371d65af652b6d4fe4
         
         обязательно подтверждать (передавать) пароль удаляемого пользователя, например:
         
         {
             "current_password": "123qwe456asd"
         }
         
         результат: удаляет токен аутентификации и вызывает удаление для данного пользователя.

12. **POST users/resend_activation/$** [name='users-resend-activation'] - повторная отправка письма для активации:

         запрос: email 
         
         Внимание! Электронное письмо не будет отправлено, если пользователь уже активен или у него нет подходящего пароля
         
         результат: регистрация пользователя, отправка письма со ссылкой для активации на почту (если is_active=False), далее снова необходимо выполнить POST 'users/activation/$'

13. **POST users/set_password/$** [name='users-set-password'] - изменение пароля авторизованного пользователя (без оправки письма по почте):

         запрос: new_password, re_new_password, current_password, например:
         
         {
             "new_password": "123qwe456asd",
             "re_new_password": "123qwe456asd",
             "current_password": "456asd123qwe"
         }
         
         результат: изменение пароля авторизованного пользователя.

14. **POST users/reset_password/$** [name='users-reset-password'] - отправка пользователю электронного письма со ссылкой для сброса пароля.

         запрос: email
      
         результат: письмо, содержащее ссылку для изменения пароля

15. **POST users/reset_password_confirm/$** [name='users-reset-password-confirm']

         запрос: из ссылки в письме, например, http://127.0.0.1:8000/users/reset_password_confirm/Mg/c6x4t4-d99843627f3f67e169f997a8a9ef6670
         
         uid: Mg, token: c6x4t4-d99843627f3f67e169f997a8a9ef6670, new_password, например:
         
         {
             "uid": "Mg",
             "token": "c6x4t4-d99843627f3f67e169f997a8a9ef6670",
             "new_password": "456asd123qwe"
         }
         
         результат: изменён пароль пользователя

16. **POST users/set_email/$** [name='users-set-username'] - изменение адреса электронной почты авторизованного пользователя:

         запрос: current_password, new_email, re_new_email, например:
         
         {
             "current_password": "123qwe456asd",
             "new_email": "don.river.2024@yandex.ru",
             "re_new_email": "don.river.2024@yandex.ru"
         }
         
         результат: изменён адрес электронной почты на новый

17. **POST users/reset_email/$** [name='users-reset-username'] - отправка пользователю электронного письма со ссылкой для сброса имени пользователя (в данном случае - электронной почты, как поля для аутентификации)
   
         запрос: email
         
         результат: письмо, содержащее ссылку для изменения имени пользователя (в данном случае - электронной почты).
         
         Внимание! После изменения электронной почты снова нужно сгенерировать токен для пользователя '/auth/token/login/',
         иначе на следующем шаге вы получите ошибку.

18. **POST users/reset_email_confirm/$** [name='users-reset-username-confirm'] - завершение процесса сброса имени пользователя (в данном случае - электронной почты)

         запрос: из ссылки в письме, например, http://127.0.0.1:8000/users/reset_email_confirm/Mg/c6x6o3-805d9e302838140009ce608ad7b2b31d
      
         uid: Mg, token: c6x6o3-805d9e302838140009ce608ad7b2b31d, new_password, например:
      
         {
             "new_email": "zaberov.dv@gmail.com"
         }
         
         результат: изменено имя пользователя (электронной почты)