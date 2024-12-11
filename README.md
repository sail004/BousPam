<h1 align="center">Серверная часть проекта Bous Pam</h1>

## Запуск проекта:

1. Клонировать репозиторий: `git clone https://github.com/sail004/BousPam`

2. Установить все необходимые библиотеки и фреймворки: `pip install -r requirements.txt`

3. Запустить приложение: `uvicorn main:app --reload`

## База данных:

### Таблица «Operations» — таблица со списком операций списания и пополнения балансов пользователей.

#### Поля:

id_operation — тип int, id операции.

id_terminal — тип int, id терминала, с которого была произведена оплата, у операций типа replenishment равен null.

bank_name — тип string, название банка, из которого было произведено пополнение кошелька, у операций типа payment равен null.

Id_user —  тип int, id пользователя, в отношении которого была проведена оплата.

type — тип string, тип операции, два варианта: payment и replenishment.

balance_change — тип float, изменение баланса в ходе операции, всегда неотрицательное значение.

datetime — тип datetime, дата проведения операции.



### Таблица «Routes» — таблица со списком маршрутов тап-тапов.

#### Поля:

id — тип int, id маршрута.

transport_company — тип string, название транспортной компании, обслуживающей маршрут.

name — тип string, название маршрута.

stops — тип string(будет изменён на array), список названий остановок, входящих в маршрут.



### Таблица «Terminals» — таблица со списком терминалов оплаты.

#### Поля:

id — тип int, id терминала.

transport_company — тип string, название транспортной компании, которой принадлежит терминал.

route — тип string, название маршрута, на котором используется терминал.



### Таблица «Transport_companies» — таблица со списком транспортных компаний.

#### Поля:

id — тип int, id транспортной компании.

name — тип string, название транспортной компании.

routes — тип string(будет изменён на array), список названий маршрутов, обслуживающихся этой транспортной компанией.

terminals — тип string(будет изменён на array), список id терминалов, принадлежащих транспортной компании.



### Таблица «Users» — таблица со списком пользователей.

#### Поля:

id — тип int, id пользователя.

name — тип string, имя пользователя.

surname — тип string, фамилия пользователя.

phone_number — тип string, номер телефона пользователя.

balance — тип float, баланс пользователя.

e_mail — тип string, электронная почта пользователя.

passport_number — тип string, номер паспорта пользователя.

snils — тип string, номер СНИЛС пользователя.

inn — тип string, номер ИНН пользователя.



## CRUD-операции:

### Register user — регистрация пользователя.

Адрес: /registration/

Json:
`
{
  "name": "string",
  "surname": "string",
  "password": "string",
  "phone_number": "string",
  "password2": "string"
}
`

Curl: 
`
curl -X 'POST' \
  'http://127.0.0.1:8000/registration/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "surname": "string",
  "password": "string",
  "phone_number": "string",
  "password2": "string"
}'
`

Request URL: http://127.0.0.1:8000/registration/

Ответы:

200 id пользователя 

200 'The number has already been registered' (если пользователь с таким номером уже зарегистрирован)


### Read users — получение списка всех пользователей.

Адрес: /users/

Json:

Curl:
`
curl -X 'GET' \
 'http://127.0.0.1:8000/users/?skip=0&limit=100' \
  -H 'accept: application/json'
`

Request URL: http://127.0.0.1:8000/users/?skip=0&limit=100

Ответы: 200 список пользователей в формате json.


### Login user — логин пользователя.

Адрес: /login/

Json:

Curl:
`
curl -X 'GET' \
 'http://127.0.0.1:8000/login/?phone_number=string&password=string' \
 -H 'accept: application/json'
`

Request URL: http://127.0.0.1:8000/login/?phone_number=string&password=string

Ответы: 200 данные пользователя в формате json при успешном логине.
		
  200 Incorrect phone number or password при неправильных данных.


### Read user by id — получить данные пользователя по его id.

Адрес: /user/{user_id}

Json:

Curl:
`
curl -X 'GET' \
  'http://127.0.0.1:8000/user/1' \
  -H 'accept: application/json'
`

Request URL: http://127.0.0.1:8000/user/1

Ответы: 200 данные пользователя в формате json.

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Update user by id — изменить данные пользователя по его id.

Адрес: /user/{user_id}

Json:
`
{
  "name": "string",
  "surname": "string",
  "password": "string",
  "phone_number": "string",
  "e_mail": "string",
  "passport_number": "string",
  "snils": "string",
  "inn": "string"
}
`

Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/user/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "surname": "string",
  "password": "string",
  "phone_number": "string",
  "e_mail": "string",
  "passport_number": "string",
  "snils": "string",
  "inn": "string"
}'
`

Request URL: http://127.0.0.1:8000/user/1

Ответы: 200

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Delete user by id — удалить пользователя по его id.

Адрес: /user/{user_id}

Json:

Curl:
`
		curl -X 'DELETE' \
  'http://127.0.0.1:8000/user/1' \
  -H 'accept: application/json'
`

Request URL: http://127.0.0.1:8000/user/1

Ответы: 200 `{
  "status": "ok",
  "message": "Deletion was successful"
}`

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Get user balance by id — получить баланс пользователя по его id.

Адрес: /balance/{user_id}

Json:

Curl:
`
		curl -X 'GET' \
  'http://127.0.0.1:8000/balance/1' \
  -H 'accept: application/json'
`

Request URL: http://127.0.0.1:8000/balance/1

Ответы: 200 баланс пользователя.

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Read operations — получить список всех операций.

Адрес: /operations/

Json:

Curl:
`
		curl -X 'GET' \
  'http://127.0.0.1:8000/operations/?skip=0&limit=100' \
  -H 'accept: application/json'
  `
  
Request URL: http://127.0.0.1:8000/operations/?skip=0&limit=100

Ответы: 200 список всех операций в формате json.


### Read operations by terminal id — получить список всех операций, проведённых конкретным терминалом по id терминала.

Адрес: /operations/{term_id}

Json:

Curl:
`
		curl -X 'GET' \
  'http://127.0.0.1:8000/operations/1' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/operations/1

Ответы: 200 список всех операций терминала в формате json.


### Read operations by user id — получить список всех операций, проведённых конкретным пользователем по id пользователя.

Адрес: /operations_user/{user_id}

Json:

Curl:
`
		curl -X 'GET' \
  'http://127.0.0.1:8000/operations_user/1' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/operations_user/1

Ответы: 200 список всех операций терминала в формате json.

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Payment by user id — провести оплату по id пользователя.

Адрес: /payment/{user_id}

Json:
`
{
  "balance_change": 0,
  "id_user": 0,
  "id_terminal": 0
}
`

Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/payment/{user_id}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "balance_change": 0,
  "id_user": 2,
  "id_terminal": 2
}'
`

Request URL: http://127.0.0.1:8000/payment/{user_id}

Ответы: 200 баланс пользователя после изменения.

404 User with id='{user_id}' not found если пользователь с таким id не найден.

404 Terminal with id='{id_terminal}' not found если терминал с таким id не найден.


### Replenishment by user id — пополнить баланс по id пользователя.

Адрес: /replenishment/{user_id}

Json: 
`
{
  "balance_change": 0,
  "id_user": 0,
 "bank_name": "string"
}
`

Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/replenishment/{user_id}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "balance_change": 0,
  "id_user": 0,
  "bank_name": "string"
}'
`

Request URL: http://127.0.0.1:8000/replenishment/{user_id}

Ответы: 200 баланс пользователя после изменения.

404 User with id='{user_id}' not found если пользователь с таким id не найден.


### Create terminal — создать терминал.

Адрес: /terminal/

Json: 
`
{
  "transport_company": "string",
  "route": "string"
}
`

Curl:
`
		curl -X 'POST' \
  'http://127.0.0.1:8000/terminal/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "transport_company": "string",
  "route": "string"
}'
`


Request URL: http://127.0.0.1:8000/terminal/

Ответы: 200 id терминала.


### Read terminal by id — получить данные терминала по его id.

Адрес: /terminal/{term_id}

Json: 

Curl:
`
		curl -X 'GET' \
  'http://127.0.0.1:8000/terminal/1' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/terminal/1

Ответы: 200 данные терминала в формате json.

404 Terminal with id='{id_terminal}' not found если терминал с таким id не найден.


### Update terminal by id — изменить данные терминала по его id.

Адрес: /terminal/{term_id}

Json: 
`
{
  "transport_company": "string",
  "route": "string"
}
`

Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/terminal/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "transport_company": "string",
  "route": "string"
}'
`


Request URL: http://127.0.0.1:8000/terminal/1

Ответы: 200.
		
404 Terminal with id='{id_terminal}' not found если терминал с таким id не найден.


### Delete terminal by id — удалить терминал по его id.

Адрес: /terminal/{term_id}

Json: 

Curl:
`
curl -X 'DELETE' \
  'http://127.0.0.1:8000/terminal/1' \
  -H 'accept: application/json'
  `
  
Request URL: http://127.0.0.1:8000/terminal/1

Ответы: 200 `{
  "status": "ok",
  "message": "Deletion was successful"
}.`

404 Terminal with id='{id_terminal}' not found если терминал с таким id не найден.


### Read terminal by company name — получить список терминалов, принадлежащих транспортной компании по её названию.

Адрес: /terminals/{company_name}

Json: 

Curl:
`
curl -X 'GET' \
  'http://127.0.0.1:8000/terminals/string' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/terminals/string

Ответы: 200 список терминалов в формате json.
		
  404 Transport company with name='{company_name}' not found если транспортная компания с таким названием не найдена.


### Create route — создать маршрут.

Адрес: /route/

Json:
`
{
  "transport_company": "string",
  "name": "string",
  "stops": "string"
}
`

Curl:
`
		curl -X 'POST' \
  'http://127.0.0.1:8000/route/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "transport_company": "string",
  "name": "string",
  "stops": "string"
}'
`

Request URL: http://127.0.0.1:8000/route/

Ответы: 200 id маршрута.


### Update route by id — обновить маршрут по его id.

Адрес: /route/{route_id}

Json:
`
{
  "transport_company": "string",
  "name": "string",
  "stops": "string"
}
`
Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/route/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "transport_company": "string",
  "name": "string",
  "stops": "string"
}'
`
Request URL: http://127.0.0.1:8000/route/1

Ответы: 200

 404 Route with id='{route_id}' not found если маршрута с таким id не существует.


### Delete route by id — удалить маршрут по его id.

Адрес: /route/{route_id}

Json: 

Curl:
`
curl -X 'DELETE' \
  'http://127.0.0.1:8000/route/1' \
  -H 'accept: application/json'
  `


Request URL: http://127.0.0.1:8000/route/1

Ответы: 200 `{
  "status": "ok",
  "message": "Deletion was successful"
}`
	
 404 Route with id='{route_id}' not found если маршрута с таким id не существует.


### Read route by route name — получить данные маршрута по его названию.

Адрес: /route/{route_name}

Json: 

Curl:
`
curl -X 'GET' \
  'http://127.0.0.1:8000/route/string' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/route/string

Ответы: 200 данные маршрута в формате json.
	
 404 Route with name='{route_name}' not found если маршрута с таким названием не существует.


### Create transport company — создать транспортную компанию.

Адрес: /tc/

Json: 
`
{
  "name": "string",
  "routes": "string",
  "terminals": "string"
}
`

Curl:
`
		curl -X 'POST' \
  'http://127.0.0.1:8000/tc/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "routes": "string",
  "terminals": "string"
}'
`

Request URL: http://127.0.0.1:8000/tc/

Ответы: 200 id транспортной компании.


### Update transport company by id — изменить данные транспортной компании по её id.

Адрес: /tc/{tc_id}

Json: 
`
{
  "name": "string",
  "routes": "string",
  "terminals": "string"
}
`

Curl:
`
		curl -X 'PUT' \
  'http://127.0.0.1:8000/tc/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "routes": "string",
  "terminals": "string"
}'
`

Request URL: http://127.0.0.1:8000/tc/1

Ответы: 200
	
 404 Company with id='{tc_id}' not found если транспортной компании с таким id не существует.


### Delete transport company by id — удалить транспортную компанию по её id.

Адрес: /tc/{tc_id}

Json: 

Curl:
`
		curl -X 'DELETE' \
  'http://127.0.0.1:8000/tc/1' \
  -H 'accept: application/json'
  `

Request URL: http://127.0.0.1:8000/tc/1

Ответы: 200 `{
  "status": "ok",
  "message": "Deletion was successful"
}`

404 Company with id='{tc_id}' not found если транспортной компании с таким id не существует.
