# Uranus REST API
Server runs by [Flask](http://flask.pocoo.org/) on Python 3.6.4

## Authorizing
This API is closed. Each client has own **token**. Every token is 32 bytes (256 bits) of URL-safe text string.

Example: `NWpAk_2UHa8k0AlgO4938ydeanmbclYrDiNbj_DIxfU`

## Making requests
All queries to the API must be **HTTP** like: 
```
http://194.67.211.237/<token>/
```
API supports GET, POST, PUT, DELETE requests

## Response format
For every request respons are given in form of **JSON**. Returned data contains two obligatory fields

```
{
  "ok": true,
  "code": 200
}
```

| **Field**  | **Description** |
| ------------- | ------------- |
| ok  | boolean indicator which gives information about the correctness of request |
| code  | status code. See **error_codes** section |

All data that was requested stored in **data** field. 

## Avaliable types
All object in Uranus API are represented as a JSON.

**Optional** means that field is not obligatory for all types, but still could be required for other.

### User

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| id  | `integer`  | Unique user id in the database  |
| type | `integer`  | Type of the user. See [Abstract Types](#abstract-types) section for more information |
| name | `string` | Full name of the User |
| email | `string` | Email of the user |
| password | `string` | Hashed password |
| taken_docs | `Documents` | A JSON-serialized object that represents [Documents](#documents) | 
| address | `string` | *Optional*. Home adress |
| phone | `string` | *Optional*. Mobile phone in any form |

### Document

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| id  | `integer` | Unique document id |
| type | `integer` | Type of the document. See [Abstract Types](#abstract-types) section for more information |
| title | `string` | Title of the document |
| description | `string` | Description of the document |
| authors | `Authors` | A JSON-serialized object that represents [Authors](#authors) |
| year | `integer` | Year of publishing |
| bestseller | `boolean` | Indicator whether this book is bestseller |
| reference | `boolean` | Indicates whether this book is reference|
| price | `integer` | Price of the document |
| copies | `integer` | Amount of copies of the document |
| available_copies | `integer` | Avialable copies of the document |
| genre | `string` | *Optional*. Genre of the book, article or multimedia |
| publisher | `string` | *Optional*. Publisher of the material |
| isbn | `string` | *Optional*. [ISBN](https://www.isbn-international.org/) 13 digit code |

### Author

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| id | `integer` | Unique identifier of Author |
| name | `string` | Full name of the Author |

### Client

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| token  | `string` | Unique token of the client |
| type  | `integer` | 0 - Android App, 1 - Web App |

### Documents

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| documents | `Array of Documents` | Array of the JSON-serialized object [Document](#document) |

### Authors

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| authors | `Array of the Author` | Array of the JSON-serialized object [Author](#author) |

### Users

| **field**  | **type** | **description** |
| ------------- | ------------- | ------------- |
| users | `Array of the User` | Array of the JSON-serialized object [User](#user) |

###### This types are only client representation of the types. 
###### They are changed or even did not exist on the server.
###### In general it is just description of JSON data.

## Abstract Types
### Users types

| **name**  | **represented** | **description** |
| ------------- | ------------- | ------------- |
| Librarian | **0** | Librarians can check overdue documents, manage patrons, and add/delete/modify documents |
| Teaching Stuff | **1** | Faculty, representing all the teaching body |
| Students | **2** | Students of the Uni |
| VPS | **3** | Visiting Professors are not part of the Faculty body |

### Documents types

| **name**  | **represented** | **description** |
| ------------- | ------------- | ------------- |
| Book | **0** | Books are written by one or more authors and published by a publisher. Books have a title and may exist in different editions – each published in a certain year. |
| Journal Articles | **1** | Journal articles are written by one or more authors, have a title, and are published in a certain journal. |
| Audio/Video | **2** | AV materials have a title and the list of authors. |

## Avaliable methods
All methods should be after token in requests.
Use [Query String](https://en.wikipedia.org/wiki/Query_string) to pass arguments.
Check [Making Requests](#making-requests) section.

**Boolean types shoud be represented as 'true'/'false' only.([JSON-like](http://json.org/))**

Example: `http://api/<token>/login?email=b.meyer&password=1234hashed56`
Example: `http://api/<token>/getUsers?debtors=true`

#### login
Use this method to check the correctness of inserted data

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| email  | `string`  | [User](#user) email without @innopolis.ru |
| password | `string`  | [User](#user) hashed password |

#### getUser
Use this method to fetch all [User](#user) data

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer` | [User](#user) id | 

#### getUsers
Use this method to fetch all [Users](#users)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| debtors | `boolean` | *Optional*. Fetch users who taken Documents |
| count | `integer` | *Optional*. If count empty returns all [Users](#users) |
| offset | `integer` | *Optional*. Strarting from number |

#### getGenres
Use this method to get list of all genres of books

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| count | `integer` | *Optional*. Default = 30 |


#### getDocument
Use this method to get [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer` | [Document](#document) ID |


#### getDocuments
Use this method to get [Documents](#documents)
To fetch all avaliable documents in database send empty request (with out any fields)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer` | *Optional*. If user_id is None, returns ALL documents|
| for_user | `integer` | *Optional*. Get document list from user perspective |
| count | `integer` | *Optional*. Default = 30 |
| offset | `integer` | *Optional*. Default = 0. Userfull for page creation |
| genre | `string` | *Optional*. Select Books of exact genre. |

Example request: `/getDocuments?id=1`

Example response:

 	{"code": 200, 
	  "data": [
	    {
	      "authors": "A.Konan Doyle,S.King", 
	      "bestseller": 1, 
	      "copies": 1, 
	      "date_of_return": "2018-03-15", 
	      "description": "Example book", 
	      "genre": null, 
	      "id": 1, 
	      "image": null, 
	      "isbn": "623555423", 
	      "price": 1312, 
	      "publisher": null, 
	      "reference": 0, 
	      "title": "12345G", 
	      "type": 0, 
	      "year": 1991
	    
	    }
	  ], 
	  "ok": true}

#### bookDocument
Use this method to book the [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| doc_id | `integer` | ID of the [Document](#document) |
| user_id | `integer` | ID of the [User](#user) |
* Можно добавить secret токен или хэш пароля отправлять каждый раз, для безопасности, но пока что такой задачи не стоит.


#### renewDocument
Use this method to renew the [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| doc_id | `integer` | ID of the [Document](#document) |
| user_id | `integer` | ID of the [User](#user) |


#### returnDocument
Use this method to reutrn the [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| doc_id | `integer` | ID of the [Document](#document) |
| user_id | `integer` | ID of the [User](#user) |

#### createDocument
This method could be only used by 0 type of [Users](#users)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| type | `integer` | Type of the document |
| title | `string` | The title of the document |
| authors | `string` |  String of authors separated by ','
| year | `integer` | Year of the publishing |
| description | `string` | *Optional* Description of the document |
| price | `integer` | *Optional* Price of the document |
| copies | `integer` | *Optional* Number of the copies. **Default** 1 | 
| image | `string` | *Optional* Represents link to the image |
| bestseller | `boolean` |*Optional* Indicator is this book bestseller |
| reference | `boolean` | Indicates whether this book is reference|
| publisher | `string` |*Optional* The name of Publishing House |
| genre | `string` |*Optional* Genre of the document |
| isbn | `string` |*Optional* ISBN |

Example: `/createDocument?type=0&title=How%20to%20be%20a%20rapper&authors=50cent,Eminem`

Response example: `{
  "code": 200, 
  "doc_id": 1, 
  "ok": true
}`

#### createUser
This method could be only used by 0 type of [Users](#users)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
|email| `string` | Email of the [User](#user) without @innopolis.ru | 
|passwd_hash | `string` | Password hash |
|name|`string`| [User](#user) Full name |
|type|`integer`|[User](#user) type. See [Types](#types)|
|phone|`string`|[User](#user) phone|
|address|`string`|[User](#user) address|
|user_image|`string`|*Optional*. Users image name|

Example: `/createUser?type=1&name=Tester&email=t.tester&password=test&phone=12345&address=Innotest&user_image=tets.jpg`

Response example: `{
  "code": 200, 
  "id": 3, 
  "ok": true
}`

#### changeUserData
Using this function you can change any field of the [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id  | `integer`  | Unique user id in the database  |
| type | `integer`  | *Optional* Type of the user. See [Abstract Types](#abstract-types) section for more information |
| name | `string` | *Optional* Full name of the User |
| email | `string` | *Optional* Email of the user |
| password | `string` | *Optional* Hashed password |
| taken_docs | `Documents` | *Optional* A JSON-serialized object that represents [Documents](#documents) | 
| address | `string` | *Optional*. Home adress |
| phone | `string` | *Optional*. Mobile phone in any form |

Example: `/changeUserData?id=1&name=NotTester`

Response example: `{
  "code": 200, 
  "ok": true
}`

#### changeDocumentData
Using this function you can change any field of the [Document](#document) except id field.

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id  | `integer` | Unique document id |
| type | `integer` | *Optional* Type of the document. See [Abstract Types](#abstract-types) section for more information |
| title | `string` | *Optional* Title of the document |
| description | `string` | *Optional* Description of the document |
| authors | `string` | *Optional* String of authors separated by ',' |
| image | `string` | *Optional* Represents link to the image |
| year | `integer` | *Optional* Year of publishing |
| bestseller | `boolean` | *Optional* Indicator whether this bok is bestseller |
| reference | `boolean` | Indicates whether this book is reference|
| price | `integer` | *Optional* Price of the document |
| copies | `integer` | *Optional* Amount of copies of the document |
| genre | `string` | *Optional*. Genre of the book, article or multimedia |
| publisher | `string` | *Optional*. Publisher of the material |
| isbn | `string` | *Optional*. [ISBN](https://www.isbn-international.org/) 13 digit code |

Example: `/changeDocumentData?id=4&type=1&reference=true`

#### deleteUser
Using this function you can delete any [User](#user)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer`  | Unique User ID |


#### deleteDocument
Using this function you can delete any [Document](#document)

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer`  | Unique Document ID |


#### getBriefUserInfo
This request returns three fields: Nearest Deadline, Amount of taken Documents, Amount of overdue Documents

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer`  | Unique User ID |

Example: `/getBriefUserInfo?id=2`

Response example: `{
  "code": 200, 
  "data": {
    "expired_docs_count": 1, 
    "nearest_deadline": [
      "2018-01-22", 
      "Mon, 22 Jan 2018 00:00:00 GMT"
    ], 
    "taken_docs_count": 3
  }, 
  "ok": true
}`

#### outstandingDocRequest
Drops all the queue, sends notifs to all users that took that document to urgently return.

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| id | `integer` | [Document](#Document) unique id to request |

#### search
This method returns search resulsts for all fields:

Documents Titles and Authors

|  Parameters | Type | Description|
| ------------- | ------------- | ------------- |
| q | `text` | Search request |
| id | `integer` | *Optional*. To search [Users](#users) needed id of [User](#user) type 0. Or in case of search by user.|

## Error Codes

|Code| Description |
| ------------- | ------------- |
| 401 | Dangerous SQL-Syntax |
| 419 |  Wrong user email or password|
|418 | Wrong user id |
| 422 | Wrong token of Client |
|423| User not found |
| 424 | Document not found |
| 425 | Document already exist |
| 426 | Invalid document data |
| 427 |User already exist |
| 428 | Invalid user data|
| 429 | Insufficient data to create document|
| 430 | No valid arguments to change the data |
| 431 | This document already have been taken by user |
| 432 | Can't take document |
| 433 | Document wasn't taken by this user |
| 440 | User has overdue period. Pay fees first to renew |
| 441 | Impossible to renew document |
| 501 | Server internal error|
