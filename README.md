# Clouding Car

Clouding Car is a car dealer and provides a REST API where you can create, get,
update and remove brands, customers and vehicles.

Some endpoints are not public because they need Bearer Authentication with
JSON Web Tokens (JWT) and role-based access, too.

## Installation

First, you should have Python 3.6.x or above installed in your computer, you could
install it from the [Python website](https://www.python.org/), be sure you have
PIP (Package Installer for Python), too.

After, run the following command in the root of the project.

```bash
pip install -r requirements.txt
```

Set the `SECRET_KEY` enviroment variable on your computer, the value can be random
bytes or a long and secure string.

On Linux/UNIX:

```bash
export SECRET_KEY=thisismylongsecretkey
```

On Windows (CMD):

```bat
setx SECRET_KEY thisismylongsecretkey
```

On Windows (Powershell):

```powershell
SET-VARIABLE SECRET_KEY thisismylongsecretkey
```

## Running

Execute the following command to run the project.

```bash
flask run
```

Visit [http://localhost:5000/api/v1](http://localhost:5000/api/v1)
on your browser or some REST API client.

You can set the default configuration like host, port, execution environment, etc.
By modifying the `.flaskenv` file.

## Available endpoints

| Method | Endpoint | Required body | Required authorization |
|---|---|:---:|:---:|
|POST|/auth/refresh|{"refresh_token": string}|No|
|POST|/auth/sign-in|{"username": string, "password": string}|No|
|GET|/brands/|None|No|
|GET|/brands/\<id\>|None|No|
|POST|/brands/|{"name": string}|Yes and admin role|
|GET|/cars/|None|No|
|GET|/cars/\<id\>|None|No|
|POST|/cars/|{"model": string, "brand": {"id": int}}|Yes and admin role|
|DELETE|/cars/\<id\>|None|Yes and admin role|
|GET|/customers/|None|Yes|
|GET|/customers/\<id\>|None|Yes|
|POST|/customers/|{"fullname": string}|Yes and admin or salesperson role|
|PUT|/customers/\<id\>|{"fullname": string}|Yes and admin or salesperson role|
|DELETE|/customers/\<id\>|None|Yes and admin role|

> This project was inspired by [blohinn/flask-restplus-full-todo-example-with-jwt](https://github.com/blohinn/flask-restplus-full-todo-example-with-jwt)
> and was explained on [September 11th, 2020 at the Pycon Bolivia meetup](https://youtu.be/vU39UOF-xG8)
